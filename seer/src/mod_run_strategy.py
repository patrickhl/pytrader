import stock_analysis as sa
import multiprocessing

class mod_run_strategy_process (multiprocessing.Process):
    def __init__(self, stock_code,till_date,strategy_mask,force_eval):
        multiprocessing.Process.__init__(self)
        self.stock_code = stock_code
        self.till_date = till_date
        self.strategy_mask = strategy_mask
        self.force_eval = force_eval
    def run(self):
        mod_run_strategy(self.stock_code,self.till_date,self.strategy_mask,self.force_eval)

def mod_run_strategy(stock_code,till_date,strategy_mask,force_eval):
    # run evaluation for the stock on the data before the start_date
    #print stock_code,' ',till_date,' ',force_eval
    sa.eval_strategy1(stock_code,till_date,force_eval)


    return 0