from pyteal import *
import program
def approval():
    global_counter = Bytes("counter") # uint64
    global_owner = Bytes("owner") # bytes
    
    op_increment = Bytes("increment")
    op_decrement = Bytes("decrement")
    
    scr_counter = ScratchVar(TealType.uint64)
    
    increment=Seq(
        App.globalPut(global_counter, App.globalGet(global_counter) + Int(1)),
        Approve()
    )
    
    decrement=Seq(
        scr_counter.store(App.globalGet(global_counter)),
        If(scr_counter.load() > Int(0)
           )
        .Then(
            App.globalPut(global_counter, App.globalGet(global_counter) - Int(1))
        ),
        Approve()
    )
    
    return program.event(
        init=Seq(
            # create a variable
            App.globalPut(global_counter, Int(0)),
            # App.globalPut(global_owner, Bytes("Me")),
            App.globalPut(global_owner, Txn.sender()),    
            Approve()     
        ),
        no_op=Cond(
            [Txn.application_args[0] == op_increment, increment],
            [Txn.application_args[0] == op_decrement, decrement]
        )
    )
def clear():
    return Approve()
