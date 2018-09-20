import stockanalysis as sa
import glbdata

def mod_update_pos(current_date):
    # This is the main schedule module that invoke trading according to the
    # evaluation results.
    # One can focus on the evaluation development.
    # The scheduler will manage the combination to keep the highest profit

    # check the evaluation result
    # update position accordingly

    new_len = glbdata.new_position.size/3
    old_len = glbdata.position.size/3

    # 1st round, update already exists position and buy new position
    for i in range(1,new_len):
        add_pos = 1
        new_code = glbdata.new_position.get_value(i, 'CODE')
        new_vol = glbdata.new_position.get_value(i, 'VOL')
        new_price = glbdata.new_position.get_value(i, 'PRICE')
        for j in range(1,old_len):
            old_code = glbdata.position.get_value(j, 'CODE')
            old_vol = glbdata.position.get_value(j, 'VOL')
            if (old_code == new_code):
                # update this position
                add_pos = 0
                if (new_vol<old_vol):
                    sa.mod_trading(new_code, 'sell_wp', (old_vol-new_vol), new_price, 0.05,current_date)
                elif (new_vol>old_vol):
                    sa.mod_trading(new_code, 'buy_wp', (new_vol-old_vol), new_price, 0.05,current_date)
                else:
                    continue
                break

        if (add_pos==1):
            # buy new position
            sa.mod_trading(new_code, 'buy_wp', (new_vol), new_price, 0.05,current_date)



    # 2nd round, clean non-existing position (in new_position list)
    while (glbdata.position.size/3>glbdata.new_position.size/3) :
        for i in range(1,glbdata.position.size/3):
            old_code = glbdata.position.get_value(i, 'CODE')
            clean_pos = 1
            for j in range(1,glbdata.new_position.size/3):
                new_code = glbdata.new_position.get_value(j, 'CODE')
                if (old_code == new_code):
                    clean_pos = 0
                    break

            if (clean_pos==1):
                sa.mod_trading(old_code, 'sell_all', 0.0, 0.0, 0.05,current_date)
                break




    return 0
