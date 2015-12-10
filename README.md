# Nagios Mattermost Plugin
A plugin for Nagios to enable notifications to Mattermost Open Source Chat.

# Usage
Assuming you are using Nagios 4, the steps are:

1. Copy _mattermost.py_ to /usr/local/nagios/libexec.
2. Create the notification command:
        define command {
              command_name notify-service-by-mattermost
              command_line /usr/local/nagios/libexec/mattermost.py --url [URL] --hostalias "$HOSTNAME$" --notificationtype "$NOTIFICATIONTYPE$" --servicedesc "$SERVICEDESC$" --servicestate "$SERVICESTATE$" --serviceoutput "$SERVICEOUTPUT$"
        }

        define command {
              command_name notify-host-by-mattermost
              command_line /usr/local/nagios/libexec/mattermost.py --url [URL] --hostalias "$HOSTNAME$" --notificationtype "$NOTIFICATIONTYPE$" --hoststate "$HOSTSTATE$" --hostoutput "$HOSTOUTPUT$"
        }
3. Create the contact:
        define contact {
          contact_name                             mattermost
          alias                                    Mattermost
          service_notification_period              24x7
          host_notification_period                 24x7
          service_notification_options             w,u,c,r
          host_notification_options                d,r
          service_notification_commands            notify-service-by-mattermost
          host_notification_commands               notify-host-by-mattermost
        }

4. Add the contact to a contact group:
        define contactgroup{
            contactgroup_name   network-admins
            alias               Network Administrators
            members             email, mattermost
        }
