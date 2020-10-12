from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from netmiko import ConnectHandler
from genie.utils import Dq
from jinja2 import Template
import csv
from alive_progress import alive_bar
import time
from netmiko import redispatch


csv_file_branch_ip='/home/shebin/NETDEVOPS/Net_automation_Project/Netmiko_Projects/Netmiko_Jinja_Config_Push/branch_ip.csv'
config_file_dir='/home/shebin/NETDEVOPS/Net_automation_Project/Netmiko_Projects/Netmiko_Jinja_Config_Push/'
jinja_template_file='/home/shebin/NETDEVOPS/Net_automation_Project/Netmiko_Projects/Netmiko_Jinja_Config_Push/branch_temp.j2'


lines =open(csv_file_branch_ip)
num_rows = len(lines.readlines())


with open(jinja_template_file)as jinja_temp:
    template_read = Template(jinja_temp.read())


console = Console()

table = Table(title='[bold] Configuration Result [/bold]')
table.add_column('Sol_ID',justify='center',style='yellow')
table.add_column('Ip_Address',justify='center',style='blue')
table.add_column('Config_Result',justify='center',style='green')

config_unsuccess = ' :cross_mark: '
config_success   = ' :white_heavy_check_mark: '

console.print(Panel('WELCOME To IDBI BANK '),justify='center',style='bold green')
console.print()
console.print('[bold]Starting with the Execution[/bold]',justify='center',style='blue on black')
console.print('[red][bold][blink] Caution[/red][/bold][/blink] - [red][bold] Do not press any key',justify='center')
console.print()


def After_Intermediate_Server_Login(ais_id,ais_ip,ais_name,ais_cfile):
    net_connect.write_channel('shebin')
    net_connect.write_channel('\n')
    redispatch(net_connect,device_type='cisco_ios')
    console.print('[bold][blue] Connecting to device with Sol_Id-> [/bold][/blue]'+ais_id,style='bold purple')
    console.print('[bold][blue] Branch-> [/bold][/blue]'+ais_name,style='bold purple')
    console.print('[bold][blue] IP-> [/bold][/blue]'+ais_ip,style='bold purple')
    console.print(Panel('Connected ! :smiley: '),style='bold green')
    console.print(Panel('[yellow][bold]Pushing configuration to the device'))
    net_connect.send_config_from_file(config_file=ais_cfile,enter_config_mode=True)
    console.print(Panel('Configuration Push Successfully !!!',style='bold green'))
    table.add_row(ais_id,ais_ip,config_success)

                



def Non_Connecting_Hosts(hname,hid,):
    file = open('Log_file_device not configured','a+')
    file.write("Configuration not pushed in "+hname+'with ip address'+hid)
    file.close()
    

with alive_bar(num_rows-1 ,length=50) as bars:

    with open(csv_file_branch_ip,'r')as br:
        csv_dict_read=csv.DictReader(br)
        for row in csv_dict_read:
            sol_id      = row['Sol_Id']
            branch_name = row['Branch']
            lan_ip      = row['Lan_IP']
            loop_ip     = row['Loopback_IP']
            lan_net     = row['Lan_Net']
            wild_card   = row['Wild_Card']
            jump_server={'device_type':'terminal_server','ip':'192.168.4.133','username':'shebin','password':'shebin123','global_delay_factor':1}
            
            config_str=''

            template_render = template_read.render(lan_network=lan_net,wildcard=wild_card)
            Final_config_str = config_str + template_render
            config_push_file = config_file_dir+sol_id+'_'+branch_name+'.txt'

            with open(config_push_file,'w')as conf_wr:
                conf_wr.write(Final_config_str)

            try:
                net_connect= ConnectHandler(**jump_server)
                net_connect.write_channel('ssh shebin@'+row['Lan_IP'])
                #net_connect.write_channel('\n')
                write_channel_op_1=net_connect._read_channel_timing(delay_factor=1,max_loops=150)
                write_channel_op_2=net_connect._read_channel_timing(delay_factor=1,max_loops=150)
                prompt_find_1=net_connect.find_prompt()
                print('Op 1=',write_channel_op_1)
                print('Op 2=',write_channel_op_2)
                print('proompt_1=',prompt_find_1)
                if ('No route to host') in  write_channel_op_2:
                    Non_Connecting_Hosts(hname=branch_name,hid=sol_id)
                    table.add_row(sol_id,branch_name,config_unsuccess)

                elif ('Connection timed out') in write_channel_op_2:
                    Non_Connecting_Hosts(hname=branch_name,hid=sol_id)
                    table.add_row(sol_id,branch_name,config_unsuccess)

                elif (("Are")or('ARE')) in prompt_find_1:
                    net_connect.write_channel('yes')
                    prompt_find_2 = net_connect.find_prompt()
                    print('channel2=',prompt_find_2)
                    if (('Password:')or('Password:')or('PASSWORD:')) in prompt_find_2:
                        After_Intermediate_Server_Login(ais_cfile=Final_config_str,ais_id=sol_id,ais_name=branch_name,ais_ip=lan_ip)
                        bars()
                        table.add_row(sol_id,branch_name,config_success)
                    else:
                        print("password failed")
    
                elif (('Password:')or('PASSWORD:')or('password:')) in prompt_find_1:
                    print("in")
                    After_Intermediate_Server_Login(ais_cfile=config_push_file,ais_id=sol_id,ais_name=branch_name,ais_ip=lan_ip)
                    bars()
                    table.add_row(sol_id,branch_name,config_success)

                else:
                    print("not moving inside are")
                    bars()
                    table.add_row(sol_id,branch_name,config_unsuccess)

                net_connect.disconnect()
   



            except Exception:
                    console.print('[bold][red]Encounter an error')
                    console.print()
                    console.print('Configuration will not be pushed into this device',style='blue on black',justify='center')
        
                    table.add_row(sol_id,branch_name,config_unsuccess)
                    bars()

                        

            del(config_str)
            console.print()
            console.print('**********'*20,style='bold green')




console.print()
console.print('Final result of successfull and unsuccesful configuration push')
console.print(table)





             
            
            