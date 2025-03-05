import subprocess
import pymysql

db = pymysql.connect(
    host="localhost",
    db="proxy_server",
    user="admin",
    passwd="123456"
)

cs = db.cursor(pymysql.cursors.DictCursor)

cs.execute("SELECT * FROM frp_manage WHERE status=1")
results = cs.fetchall()

for result in results:
    task_id = result.get("id")
    process_id = result.get("process_id")
    client_name = result.get("client_name")

    command = f"ps -ef | grep {process_id} | grep -c -v grep"
    active_process = subprocess.getstatusoutput(command)

    if int(active_process[1]) < 1:
        cmd = f"nohup /home/ubuntu/proxyServer/frp_tools/frps -c /home/ubuntu/proxyServer/frp_client/{client_name}_frps.ini > /dev/null 2>&1 &"
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        pid = process.pid + 1

        query = "update frp_manage set process_id = %s WHERE id = %s"
        cs.execute(query, (pid, task_id))
        db.commit()

db.close()
