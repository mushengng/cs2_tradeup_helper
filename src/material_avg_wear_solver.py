from decimal import Decimal, getcontext, InvalidOperation

#设置精度为50位，确保17位小数运算无误差
getcontext().prec = 50

try:
    #输入所有参数
    material_min = Decimal(input("请输入材料最小磨损: "))
    material_max = Decimal(input("请输入材料最大磨损: "))
    product_min = Decimal(input("请输入产物最小磨损: "))
    product_max = Decimal(input("请输入产物最大磨损: "))
    product_final = Decimal(input("请输入产物最终磨损: "))

    #公式推导求解x
    A = product_final - product_min
    B = product_max - product_min
    if B == 0:
        raise ZeroDivisionError("产物最大磨损与最小磨损不能相等")
    C = material_max - material_min
    x = material_min + (A / B) * C
    #输出结果并强制保留17位小数
    print(f"\n计算得到的材料平均磨损为: {x:.17f}")
    input("\n按Enter结束")

except ZeroDivisionError as e:
    print(f"错误: {e}")

except InvalidOperation:
    print("错误: 输入不是有效的数字")

except EOFError:
    print("\n输入已中断")

except KeyboardInterrupt:
    print("\n程序被用户中断")