import stock_analysis as sa
import pandas as pd
import glbdata
import string
import sys

def mod_schedule(max_stock,min_stock,start_date):
    # This is the main schedule module that invoke trading according to the
    # evaluation results.
    # One can focus on the evaluation development.
    # The scheduler will manage the combination to keep the highest profit
    if __name__ == '__main__':
        standard_data = pd.read_csv('../data/' + '000001' + '/hist_k_day.csv')
        code_list = pd.read_csv('../data/stock_code.csv')
        date_list = standard_data['date']
        valid_list = pd.read_csv('../data/stock_code_validation.csv')

        date_acc = 0
        stock_acc = 0
        processes = []
        force_eval = True
        # check the evaluation result
        # update position accordingly

        # timing axis
        for i in range(date_list.size):
            date = date_list.get_value(i,'date')
            if (string.atoi(start_date[0:4]+start_date[5:7]+start_date[8:10]) <= string.atoi(date[0:4]+date[5:7]+date[8:10])):
                #print "hit date"
                date_acc = date_acc + 1
                stock_acc= 0
                # evaluate all stocks
                for j in range(code_list.size/2):
                    code = code_list.get_value(j,'CODE')
                    validation = False
                    # check validation
                    for k in range(valid_list.size/3):
                        if (valid_list.get_value(k,'CODE')==code):
                            validation = valid_list.get_value(k,'VALID')
                            break

                    if (code>=600000 and code<600200 and validation):
                        #print "hit code"
                        stock_acc = stock_acc + 1
                        if (stock_acc % 100 == 0):
                            print "date_acc:",str(date_acc),"stock_add:",stock_acc

                        if (date_acc==1):
                            sa.mod_run_strategy(str(code),date,0,force_eval)
                        else:
                            process = sa.mod_run_strategy_process(str(code),date,0,force_eval)
                            process.start()
                            processes.append(process)
                    else:
                        continue

                if (date_acc>1):
                    for p in processes:
                        p.join()

                #print "after run_strategy"
                sa.mod_pickup_pos(max_stock,min_stock,date)
                #print "after pickup"
                sa.mod_update_pos(date)
                #print "after update pos"

                if (date_acc%10==1):
                    sa.rpt_total_capital(date)

                force_eval = False
            else:
                continue

    return 0





