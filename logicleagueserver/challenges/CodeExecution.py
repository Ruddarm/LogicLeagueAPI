import io
import time
import tarfile
from .Containerpool import  container_pool
from .models import TestCase , Solution
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
        return [None,'.py',"/bin/sh -c 'python3 /sandbox/Solution.py < /sandbox/input.txt 2> /sandbox/error.log'"]
    elif lang== "java":
        return ["/bin/sh -c 'javac Solution.java 2> /sandbox/error.log '",'.java', "/bin/sh -c 'java Solution < /sandbox/input.txt 2> /sandbox/error.log'"]
    elif lang == "javascript":
        return [None,".js","/bin/sh -c 'node /sandbox/Solution.js < /sandbox/input.txt 2> /sandbox/error.log'"]
    else :
        raise languageError("unsupported language")
def run_code(code,language, challenge_id):
    """ Run code for given challenge id.
        this funciotn will compile the given code if language eixsit or else it will throw erro lang not foun d
        It will run the code and test with the sample testcases 
        

    Args:
        code (str): code submitied by user
        language (str): langue of the give code 
        challenge_id (uuid): Challenge id for which the code is supposed to run 

    Returns:
        result : result will contain output , error, testcases  
    """
    output=""
    error=""
    iserror=False
    try:
        complie_cmd, extension , exe_cmd = get_cmd_lang(language);
        # filename
        filename = f'Solution{extension}'
        # get container
        container = container_pool.get_container()
        # put code in container
        container.put_archive("/sandbox", create_tarball(code=code, file_name=  filename))
        # put error log file in container
        container.put_archive("/sandbox",create_tarball(code="",file_name="error.log"))
        # if progming lang required compilation
        if complie_cmd:
            exec_result = container.exec_run(complie_cmd)
            if exec_result.exit_code!=0:
                error = container.exec_run("cat /sandbox/error.log").output.decode('utf-8');
                iserror = True
                return {"result":"","output":output,"error":error,"iserror":iserror}
        testCase = TestCase.objects.filter(challengeID=challenge_id, isSample=True)
        result  = []
        for test in testCase:
            container.put_archive("/sandbox",create_tarball(code=test.input_txt,file_name="input.txt")) 
            exec_result = container.exec_run(exe_cmd)
            output = exec_result.output.decode("utf-8")
            for i in zip(output.strip().split('\n'),test.output_txt.split('\n')):
                # print(f'output is {i[0].strip()} \n expected is {i[1].strip()}')
                if i[0].strip() == i[1].strip():
                    result.append({"testCaseId":test.testCaseID,"input":test.input,"output":test.output,"ans":i[0],"result":True});
                else :
                    result.append({"testCaseId":test.testCaseID,"input":test.input,"output":test.output,"ans":i[0],"result":False});
            # print(f'input is {test.input_txt} \n output is {output} \n')
            if exec_result.exit_code!=0:
                error = container.exec_run("cat /sandbox/error.log").output.decode('utf-8');
         
                iserror = True
                break
    except :
        raise
    finally:
        container.exec_run(f"rm -f /sandbox/{filename} /sandbox/input.txt /sandbox/error.log")
        container_pool.return_container(container=container)
    return {"result":result,"output":output,"error":error,"iserror":iserror}
        
def submit_code(code,language,challenge_instance,user_instance  ):
    output=""
    error=""
    iserror=False
    total_runtime = 0  #total run time 
    #toal number of test cases 
    total_testcases = 0 
    
    try:
        complie_cmd, extension , exe_cmd = get_cmd_lang(language);
        # filename
        filename = f'Solution{extension}'
        # get container
        container = container_pool.get_container()
        # put code in container
        container.put_archive("/sandbox", create_tarball(code=code, file_name=  filename))
        # put error log file in container
        container.put_archive("/sandbox",create_tarball(code="",file_name="error.log"))
        # if progming lang required compilation
        if complie_cmd:
            exec_result = container.exec_run(complie_cmd)
            if exec_result.exit_code!=0:
                error = container.exec_run("cat /sandbox/error.log").output.decode('utf-8');
                iserror = True
                # case 1 if compilation error
                return {"result":"","output":output,"error":error,"iserror":iserror}
        testCase = TestCase.objects.filter(challengeID=challenge_instance.challengeID)
        result  = []
        # run code for each test case
        for test in testCase:
            # increase the count of testcase
            total_testcases+=1;
            # print(f'input is {test.input_txt} \n output is {test.output_txt} \n')
            container.put_archive("/sandbox",create_tarball(code=test.input_txt,file_name="input.txt")) 
            # start time 
            start_time = time.time()
            exec_result = container.exec_run(exe_cmd)
            # end time
            end_time= time.time()
            # total time taken to complete testcase in milisecond 
            total_runtime+=(end_time-start_time)*1000
            # decoding output of run code
            output = exec_result.output.decode("utf-8")
            
            if exec_result.exit_code!=0:
                # if code got run time error
                error = container.exec_run("cat /sandbox/error.log").output.decode('utf-8');
                iserror = True
                break
            # Comapre output with expected output
            for i in zip(output.strip().split('\n'),test.output_txt.split('\n')):
                if i[0].strip() != i[1].strip():
                    result.append({"testCaseId":test.testCaseID,"input":test.input,"output":test.output,"ans":i[0],"result":False});
                    # if submisision get false for any test case
                    return {"result":result,"output":output,"error":error,"iserror":iserror,"submited":False}	
            
        solution = Solution.objects.create(code=code,language=language,challengeID=challenge_instance,userId=user_instance , runtime= total_runtime)
    except :
        raise
    finally:
        container.exec_run(f"rm -f /sandbox/{filename} /sandbox/input.txt /sandbox/error.log")
        container_pool.return_container(container=container)
    return {"result":result,"output":output,"error":error,"iserror":iserror,"submited":True}