from challenges.CodeExecution import create_tarball , get_cmd_lang
from challenges.Containerpool import container_pool
from challenges.models import TestCase, Solution, Challenge
def evalualte_submission(code,language,challenge,contest,user):
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