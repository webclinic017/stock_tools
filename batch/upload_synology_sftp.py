import pysftp
import yaml

# read from secret
def getsecret():
    with open("../secret.yaml", "r") as stream:
        try:
            data = yaml.safe_load(stream)
            host = data['synology_sftp_url']
            port = data['synology_sftp_port']
            username = data['synology_username']
            password = data['synology_password']
            return (host, port, username, password)
        except yaml.YAMLError as exc:
            print(exc)
            return None

def uploadFile(file_local_path, file_remote_dir):
    (host, port, username, password) = getsecret()

    # Accept any host key (still wrong see below)
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None

    sftp = pysftp.Connection(host, port=port, username=username, password=password, private_key=".ppk",
    cnopts=cnopts)
    sftp.chdir(file_remote_dir)
    sftp.put(file_local_path)

def downloadFile(file_remote_path, file_local_dir):
    (host, port, username, password) = getsecret()

    sftp = pysftp.Connection(host, port=port, username=username, password=password)
    sftp.cd(file_local_dir)
    sftp.get(file_remote_path)

if __name__ == '__main__':
    uploadFile("/Users/yiuminglai/GitProjects/stock_tools/README.md", '/home/')
