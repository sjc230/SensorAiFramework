import queue
from multiprocessing import Process, Queue, Manager
import threading
import psutil
import uuid

def count_threads_in_process(process):
    # Use psutil to check thread count
    process = psutil.Process(process.pid)  # Get process info by PID
    return process.num_threads()

class ProcPool:
    def __init__(self, workers=8):
        self.proc_list=[]   # a list of dictionary {"proc":p, "arg_q":proc_arg_q}
        self.theads_dict={} # {"thread_name": arg_q, }
        self.proc_return_q=Queue()
        self.rw_lock = threading.RLock()
        # manager = Manager()
        # shared_dict = manager.dict()

        if workers<1:
            workers=1
        for i in range(workers):
            proc_arg_q=Queue()
            p=Process(target=self.schedule_task, args=(proc_arg_q, self.proc_return_q, ))
            p.start()
            self.proc_list.append({"proc":p, "arg_q":proc_arg_q})
        
        mt=threading.Thread(target=self.manager_loop)
        mt.start()

    def schedule_task(self, arg_q, return_q):
        threads_list=[]
        while True:
            cmd=arg_q.get()
            print(cmd)
            if (not cmd) or ("cmd_type" not in cmd): continue
            if "thread_create"==cmd["cmd_type"]:
                thread=threading.Thread(target=cmd["task"], args=cmd["args"], kwargs=cmd["kwargs"], name=cmd["thread_name"])
                # schedule_thread = threading.Thread(target=process_schedule, args=(mqtt_msg_queue,) )
                thread.daemon = True
                thread.start()
                threads_list.append(thread)

            if "thread_alvie_check"==cmd["cmd_type"]:
                temp_list=threads_list.copy()
                for thrd in temp_list:
                    alive_status=thrd.is_alive()
                    return_q.put({thrd.name:alive_status})
                    if not alive_status:
                        threads_list.remove(thrd)

    def request_threads_alive_status(self):
        for p in self.proc_list:
            arg_q=p["arg_q"]
            arg_q.put({"cmd_type":"thread_alvie_check"})

    def manager_loop(self):
        while True:
            try:
                status=self.proc_return_q.get(timeout=3)
            except queue.Empty:
                self.request_threads_alive_status()
                continue
            print(f"status={status}")
            for th_name, alive_status in status.items():
                if alive_status==False:
                    with self.rw_lock:
                        self.theads_dict.pop(th_name)


    def new_thread(self, target, args=None, kwargs=None, name=None):
        '''
        thread_name, must be unique.[IMPORTANT], e.g MAC address
        '''
        task=target
        thread_name=name

        threads_min=99999999
        arg_q=None
        index=0
        for p in self.proc_list:
            threads=count_threads_in_process(p["proc"])
            if threads<threads_min:
                arg_q=self.proc_list[index]["arg_q"]
                threads_min=threads
            index +=1

        if arg_q:
            if thread_name is None:
                thread_name = uuid.uuid4()
            arg_q.put({"cmd_type":"thread_create", "thread_name":thread_name, "task":task, "args":args, "kwargs":kwargs})
            
            with self.rw_lock:
                self.theads_dict[thread_name]=arg_q
            return thread_name
        else:
            return None
    
    def kill_thread(self, thread_name):
        q=None
        with self.rw_lock:
            if thread_name in self.theads_dict:
                q=self.theads_dict[thread_name]

        if q is None: return

        # Clear the queue
        while not q.empty():
            try:
                q.get_nowait()  # Non-blocking
            except queue.Empty:
                break
        q.put(None)     # Send a None message to notify the thread to terminate itself
    
    def is_existed(self, thread_name):
        with self.rw_lock:
            if thread_name in self.theads_dict:
                return True
            else:
                return False

    
#============= For testing ########################
def ai_unit_process(mac_addr, seismic_data_queue, vital_queue, **kwargs):
    cnt=0
    while True:
        print(f"{mac_addr},{seismic_data_queue},{vital_queue},kwargs= {kwargs}")
        sleep(3)
        cnt +=1

        # if cnt > 5: break


if __name__ == '__main__':
    from time import sleep

    proc_pool=ProcPool(2)
    ai_kwargs={}
    ai_kwargs["dd"]=1
    ai_kwargs["ed"]=2
    ai_kwargs["dccd"]=3

    proc_pool.new_thread("11:22:33:44:55:66",ai_unit_process, ("ddd", "eee", "fff"),ai_kwargs)

    for i in range(10):
        name="test_thread" + str(i)
        proc_pool.new_thread(name,ai_unit_process, ("11", "22", "33"),ai_kwargs)
    while True:
        print("=============================")
        for i in range(10):
            name="test_thread" + str(i)
            print(f"{name}:{proc_pool.is_existed(name)}")
        sleep(1)