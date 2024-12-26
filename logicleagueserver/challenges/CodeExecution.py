import io
import tarfile
from .Containerpool import  container_pool
class languageError(Exception):
    def __init__(self, msg,*args):
        super().__init__(msg)

def create_tarball(code, file_name):
    tar_stream = io.BytesIO()
    with tarfile.open(fileobj=tar_stream, mode="w") as tar:
        file_info = tarfile.TarInfo(file_name)
        file_info.size = len(code)
        tar.addfile(file_info, io.BytesIO(code.encode('utf-8')))
    
    tar_stream.seek(0)
    return tar_stream
def get_cmd_lang(lang):
    if lang== "python":
        return ['.py',"/bin/sh -c 'python3 /sandbox/Solution.py < /sandbox/input.txt 2> /sandbox/error.log'"]
    elif lang== "java":
        return ['.java', "/bin/sh -c 'javac Solution.java 2> /sandbox/error.log  && java Solution < /sandbox/input.txt 2> /sandbox/error.log'"]
    elif lang == "javascript":
        return [".js","/bin/sh -c 'node /sandbox/Solution.js < /sandbox/input.txt 2> /sandbox/error.log'"]
    else :
        raise languageError("unsupported language")
def run_code(code,language):
    output=""
    error=""
    iserror=False
    
    try:
        extension , cmd = get_cmd_lang(language);
        filename = f'Solution{extension}'
        container = container_pool.get_container()

        container.put_archive("/sandbox", create_tarball(code=code, file_name=  filename))
        container.put_archive("/sandbox",create_tarball(code="21\n18\n",file_name="input.txt"))
        container.put_archive("/sandbox",create_tarball(code="",file_name="error.log"))
        exec_result = container.exec_run(cmd)
        output = exec_result.output.decode("utf-8")
        if exec_result.exit_code!=0:
                error = container.exec_run("cat /sandbox/error.log").output.decode('utf-8');
                iserror = True
    except :
        raise
    finally:
        container.exec_run(f"rm -f /sandbox/{filename} /sandbox/input.txt /sandbox/error.log")
        container_pool.return_container(container=container)
    return {"output":output,"error":error,"iserror":iserror}
        
    