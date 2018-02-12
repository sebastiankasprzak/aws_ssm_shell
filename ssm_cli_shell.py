import cmd
import boto3
import time
import json
import re
from botocore import exceptions


class SSMCLI(cmd.Cmd):
    """Simple command processor example."""

    prompt = "/ $ "
    intro = "SSM remote command executor"

    instance_id = ""
    instance_id_valid_flag = False
    dir = "/"
    ssm = None
    region = "eu-west-1"

    def change_prompt(self):
        """Change prompt"""
        self.prompt = "{id} {dir} $ ".format(
            id=self.instance_id,
            dir=self.dir
        )

    def check_instance_id(self, id):
        """Validate instance_id against regex match"""
        regex_expression = re.compile("(^i-(\w{8}|\w{17})$)|(^mi-\w{17}$)")
        if regex_expression.match(id):
            return True
        else:
            return False

    def do_login(self, profile_name):
        """Authenticate to customer AWS API with a profile stored in ~/.aws/config"""
        if not profile_name:
            print("You have to provide name of AWS profile!")
        else:
            try:
                session = boto3.Session(profile_name=profile_name)
                self.ssm = session.client('ssm', region_name=self.region)
                print("Logged in to {} successfully".format(profile_name))
            except exceptions.ProfileNotFound:
                print("Profile {} does not exist!".format(profile_name))
                pass

    def do_region(self, region):
        """Set AWS region, by default it is set to eu-west-1"""
        if not region:
            print("You have to provide region name!")
        else:
            self.region = region
            print("Region set to {}".format(region))

    def do_set_instance_id(self, instance_id):
        """Set instance id"""
        if not instance_id:
            print("You have to supply instance id!")
            return False

        if self.check_instance_id(id=instance_id):
            self.instance_id = instance_id
            self.instance_id_valid_flag = True
            print("Instance ID is {}".format(instance_id))
            self.change_prompt()
        else:
            print("Instance ID {} is not valid and it has NOT been saved!".format(instance_id))

    def do_cd(self, dir):
        """Change currently working directory"""
        # TODO: validate the directory supplied
        self.dir = dir
        print("Changed directory to {}".format(dir))
        self.change_prompt()

    def do_shell(self, cmd):
        """Execute command"""
        if not self.ssm:
            print("You have not logged in to any account!")
            return False

        if not self.instance_id_valid_flag:
            print("Currently set instance_id {} is not valid!".format(self.instance_id))
            return False

        try:
            ssm_cmd = self.ssm.send_command(
                InstanceIds=[
                    self.instance_id
                ],
                DocumentName="AWS-RunShellScript",
                TimeoutSeconds=30,
                Parameters={
                    "workingDirectory": [
                        self.dir
                    ],
                    "executionTimeout": [
                        "3600"
                    ],
                    "commands": [cmd]
                }
            )
        except exceptions.ClientError as e:
            print(e)
            return False

        command_id = ssm_cmd["Command"]["CommandId"]

        cmd_status = self.ssm.list_commands(
            CommandId=command_id,
            InstanceId=self.instance_id
        )["Commands"][0]["Status"]

        while cmd_status == "Pending" or cmd_status == "InProgress":
            cmd_status = self.ssm.list_commands(
                CommandId=command_id,
                InstanceId=self.instance_id
            )["Commands"][0]["Status"]
            print(cmd_status)
            time.sleep(0.5)

        out = self.ssm.get_command_invocation(
            CommandId=command_id,
            InstanceId=self.instance_id
        )

        if out["Status"] == "Success":
            print(out["StandardOutputContent"])
        elif out["Status"] == "Failed":
            print(out["StandardErrorContent"])
        else:
            print(json.dumps(out, indent=2))

    def do_end(self, line):
        print("Bye bye")
        return True


if __name__ == '__main__':
    SSMCLI().cmdloop()
