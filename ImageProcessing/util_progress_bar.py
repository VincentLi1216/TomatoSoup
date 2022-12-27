def progress_bar(now, total, total_blocks = 50, decimal_point = 2, last_percent = 1):

    if now == total or now/total >= last_percent:
        print(
            f'\r[{"█"*total_blocks}] {100}%',end='')  # 輸出不換行的內容
    else:
        total_blocks = total_blocks
        plus_block = "█" * int(now * total_blocks / total)
        minus_block = " " * int(total_blocks - int(now * total_blocks / total))
        percentage = round(now * 100 / total, decimal_point)
        print(f'\r[{plus_block}{minus_block}] {percentage}%',end='')  # 輸出不換行的內容