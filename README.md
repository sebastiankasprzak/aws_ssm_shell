# SSM Remote Shell Executor
An idea for simple adaptation of "shell" like behaviour for EC2 instances running AWS SSM agent. Although with limitations, this solutions presents an alternative to classic "bastion" solution for accessing shell of Linux EC2 instances.

### Main benefits:
- no requirement for layer 3 connectivity to the instances, only API level access is required
- no additional infrastructure required, just SSM agent bootstrapped on all instances in the environment
- ability to easily manage workloads in multiple AWS accounts and environments
- auditing possible via Cloudtrail and SSM's ability to report command outputs to S3 buckets

### Current limitations
- It is not possible to use any straming commands (i.e. `top`, `tail -f`, etc)
- 2500 characters limit in output
- careful around API request limits

## Basic Usage
### Initial setup
Clone the repo, install dependencies: `pip install -r requirements.txt`.

Setup AWS profile using `aws configure --profile {profile_name}`

### Usage

    $ python ssm_cli_shell.py
    SSM remote command executor
    / $ help
    
    Documented commands (type help <topic>):
    ========================================
    cd  help  login  region  set_instance_id  shell
    
    Undocumented commands:
    ======================
    end
    
    / $ login aws-profile-1  # profile has to exist in ~/.aws/ folder
    Logged in to aws-profile-1 successfully
    / $ set_instance_id i-12345abcde
    Instance ID is i-12345abcde
    i-12345abcde / $cd /var/log
    Changed directory to /var/log
    i-12345abcde /var/log $!ls -l
    InProgress
    InProgress
    Success
    total 784
    drwxr-xr-x 3 root root   4096 Feb  7 09:59 amazon
    drwx------ 2 root root   4096 Feb  7 09:59 audit
    -rw------- 1 root root      0 Feb  7 09:59 boot.log
    -rw------- 1 root utmp      0 Jan 15 18:42 btmp
    -rw-r--r-- 1 root root   7651 Feb 12 08:05 cloud-init-output.log
    -rw-r--r-- 1 root root 263913 Feb 12 08:05 cloud-init.log
    -rw------- 1 root root    818 Feb 12 10:01 cron
    -rw------- 1 root root  13365 Feb 12 09:12 cron-20180212
    -rw-r--r-- 1 root root  23223 Feb 12 08:05 dmesg
    -rw-r--r-- 1 root root  23223 Feb  9 08:05 dmesg.old
    -rw-r--r-- 1 root root 102703 Jan 15 18:43 dracut.log
    -rw-r--r-- 1 root root 146292 Feb  7 12:35 lastlog
    drwxr-xr-x 2 root root   4096 Jan 15 18:42 mail
    -rw------- 1 root root      0 Feb 12 09:12 maillog
    -rw------- 1 root root    764 Feb 12 08:05 maillog-20180212
    -rw------- 1 root root   3767 Feb 12 10:08 messages
    -rw------- 1 root root 259140 Feb 12 09:10 messages-20180212
    drwxr-xr-x 2 ntp  ntp    4096 Apr 19  2017 ntpstats
    -rw------- 1 root root      0 Feb 12 09:12 secure
    -rw------- 1 root root   2724 Feb 12 08:05 secure-20180212
    -rw------- 1 root root      0 Feb 12 09:12 spooler
    -rw------- 1 root root      0 Jan 15 18:42 spooler-20180212
    -rw------- 1 root root      0 Jan 15 18:42 tallylog
    -rw-rw-r-- 1 root utmp  26880 Feb 12 08:05 wtmp
    -rw------- 1 root root    125 Feb  7 10:00 yum.log
    
    i-12345abcde /var/log $!tail -n 50 messages
    InProgress
    Success
    Feb 12 09:12:01 ip-10-210-1-38 rsyslogd: [origin software="rsyslogd" swVersion="5.8.10" x-pid="2276" x-info="http://www.rsyslog.com"] rsyslogd was HUPed
    Feb 12 09:12:38 ip-10-210-1-38 dhclient[2197]: XMT: Solicit on eth0, interval 113790ms.
    Feb 12 09:14:32 ip-10-210-1-38 dhclient[2197]: XMT: Solicit on eth0, interval 124830ms.
    Feb 12 09:16:37 ip-10-210-1-38 dhclient[2197]: XMT: Solicit on eth0, interval 129980ms.
    Feb 12 09:18:47 ip-10-210-1-38 dhclient[2197]: XMT: Solicit on eth0, interval 126250ms.
    Feb 12 09:20:54 ip-10-210-1-38 dhclient[2197]: XMT: Solicit on eth0, interval 109130ms.
    Feb 12 09:22:43 ip-10-210-1-38 dhclient[2197]: XMT: Solicit on eth0, interval 118060ms.
    Feb 12 09:24:41 ip-10-210-1-38 dhclient[2197]: XMT: Solicit on eth0, interval 125410ms.
    Feb 12 09:26:37 ip-10-210-1-38 dhclient[2095]: DHCPREQUEST on eth0 to 10.210.1.1 port 67 (xid=0x6ba28512)
    Feb 12 09:26:37 ip-10-210-1-38 dhclient[2095]: DHCPACK from 10.210.1.1 (xid=0x6ba28512)
    Feb 12 09:26:37 ip-10-210-1-38 dhclient[2095]: bound to 10.210.1.38 -- renewal in 1448 seconds.
    Feb 12 09:26:37 ip-10-210-1-38 ec2net: [get_meta] Trying to get http://169.254.169.254/latest/meta-data/network/interfaces/macs/06:8a:df:29:23:c2/local-ipv4s
    Feb 12 09:26:37 ip-10-210-1-38 ec2net: [rewrite_aliases] Rewriting aliases of eth0
    Feb 12 09:26:46 ip-10-210-1-38 dhclient[2197]: XMT: Solicit on eth0, interval 127290ms.
    Feb 12 09:28:54 ip-10-210-1-38 dhclient[2197]: XMT: Solicit on eth0, interval 110280ms.
    Feb 12 09:30:44 ip-10-210-1-38 dhclient[2197]: XMT: Solicit on eth0, interval 123200ms.
    Feb 12 09:32:47 ip-10-210-1-38 dhclient[2197]: XMT: Solicit on eth0, interval 114310ms.
    Feb 12 09:34:42 ip-10-210-1-38 dhclient[2197]: XMT: Solicit on eth0, interval 119370ms.
    Feb 12 09:36:41 ip-10-210-1-38 dhclient[2197]: XMT: Solicit on eth0, interval 120810ms.
    Feb 12 09:38:42 ip-10-210-1-38 dhclient[2197]: XMT: Solicit on eth0, interval 127370ms.
    Feb 12 09:40:50 ip-10-210-1-38 dhclient[2197]: XMT: Solicit on eth0, interval 127660ms.
    Feb 12 09:42:57 ip-10-210-1-38 dhclient[2197]: XMT: Solicit on eth0, interval 125800ms.
    Feb 12 09:45:03 ip-10-210-1-38 dhclient[2197]: XMT: Solicit on eth0, interval 130280ms.
    Feb 12 09:47:14 ip-10-210-1-38 dhclient[2197]: XMT: Solicit on eth0, interval 110270ms.
    Feb 12 09:49:04 ip-10-210-1-38 dhclient[2197]: XMT: Solicit on eth0, interval 108420ms.
    Feb 12 09:50:45 ip-10-210-1-38 dhclient[2095]: DHCPREQUEST on eth0 to 10.210.1.1 port 67 (xid=0x6ba28512)
    Feb 12 09:50:45 ip-10-210-1-38 dhclient[2095]: DHCPACK from 10.210.1.1 (xid=0x6ba28512)
    Feb 12 09:50:45 ip-10-210-1-38 dhclient[2095]: bound to 10.210.1.38 -- renewal in 1559 seconds.
    Feb 12 09:50:45 ip-10-210-1-38 ec2net: [get_meta] Trying to get http://169.254.169.254/latest/meta-data/network/interfaces/macs/06:8a:df:29:23:c2/local-ipv4s
    Feb 12 09:50:45 ip-10-210-1-38 ec2net: [rewrite_aliases] Rewriting aliases of eth0
    Feb 12 09:50:52 ip-10-210-1-38 dhclient[2197]: XMT: Solicit on eth0, interval 118920ms.
    Feb 12 09:52:52 ip-10-210-1-38 dhclient[2197]: XMT: Solicit on eth0, interval 112880ms.
    Feb 12 09:54:44 ip-10-210-1-38 dhclient[2197]: XMT: Solicit on eth0, interval 126470ms.
    Feb 12 09:56:51 ip-10-210-1-38 dhclient[2197]: XMT: Solicit on eth0, interval 124250ms.
    Feb 12 09:58:55 ip-10-210-1-38 dhclient[2197]: XMT: Solicit on eth0, interval 122670ms.
    Feb 12 10:00:58 ip-10-210-1-38 dhclient[2197]: XMT: Solicit on eth0, interval 110230ms.
    Feb 12 10:02:48 ip-10-210-1-38 dhclient[2197]: XMT: Solicit on eth0, interval 117280ms.
    Feb 12 10:04:46 ip-10-210-1-38 dhclient[2197]: XMT: Solicit on eth0, interval 111060ms.
    Feb 12 10:06:37 ip-10-210-1-38 dhclient[2197]: XMT: Solicit on eth0, interval 122050ms.
    Feb 12 10:08:39 ip-10-210-1-38 dhclient[2197]: XMT: Solicit on eth0, interval 129440ms.
    
    i-12345abcde /var/log $
    

## Future work:
- discovery and autocompletion of profiles and instances in the AWS account
- windows/powershell support
- exception/error handling
- auditing
