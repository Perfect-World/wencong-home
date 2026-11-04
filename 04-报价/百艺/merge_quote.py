import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from collections import OrderedDict

wb = openpyxl.load_workbook('/Users/wencong/Documents/房/home/04-报价/百艺/基础最新报价.xlsx', data_only=True)
ws = wb['Page 1']

# 提取所有有效项目行（跳过小计、标题、说明等）
skip_names = {'工程项目或费用名称', '此项小计', '基础工程直接费', '基础工程管理费', '制图费', '基础工程造价'}
projects = OrderedDict()

for row in ws.iter_rows(min_row=6, max_row=ws.max_row, values_only=True):
    name = row[4] if len(row) > 4 and row[4] else None
    unit = row[9] if len(row) > 9 else None
    qty = row[10] if len(row) > 10 else None
    price = row[11] if len(row) > 11 else None
    total = row[12] if len(row) > 12 else None

    if not name or not isinstance(name, str):
        continue
    name = name.strip().replace('\n', '')
    if name in skip_names or name.startswith('一、') or name.startswith('二、') or name.startswith('三、') \
        or name.startswith('四、') or name.startswith('五、') or name.startswith('六、') or name.startswith('七、') \
        or name.startswith('八、') or name.startswith('九、') or name.startswith('十、') \
        or name.startswith('1.') or name.startswith('2.') or name.startswith('3.') or name.startswith('4.') \
        or name.startswith('5.') or name.startswith('6.') or name.startswith('7.') or name.startswith('8.') or name.startswith('9.'):
        continue
    if qty is None and total in (0, None, '0'):
        continue

    key = name
    if key not in projects:
        projects[key] = {'unit': unit, 'total_qty': 0, 'price': price, 'total_amount': 0, 'count': 0}
    if isinstance(qty, (int, float)):
        projects[key]['total_qty'] += qty
    if isinstance(total, (int, float)):
        projects[key]['total_amount'] += total
    projects[key]['count'] += 1

# 创建新工作簿
wb_new = openpyxl.Workbook()
ws_new = wb_new.active
ws_new.title = '按项目合并汇总'

# 样式定义
HEADER_FILL = PatternFill(fill_type='solid', fgColor='4472C4')
HEADER_FONT = Font(bold=True, color='FFFFFF', size=11)
TITLE_FONT = Font(bold=True, size=14)
ZEBRA_FILL_1 = PatternFill(fill_type='solid', fgColor='FFFFFF')
ZEBRA_FILL_2 = PatternFill(fill_type='solid', fgColor='F2F2F2')
TOTAL_FILL = PatternFill(fill_type='solid', fgColor='FFF2CC')
TOTAL_FONT = Font(bold=True)
THIN_BORDER = Border(
    left=Side(style='thin', color='D9DEE7'),
    right=Side(style='thin', color='D9DEE7'),
    top=Side(style='thin', color='D9DEE7'),
    bottom=Side(style='thin', color='D9DEE7'),
)

# 标题
ws_new.merge_cells('A1:E1')
ws_new['A1'] = '百艺装饰基础工程报价 - 按项目合并汇总'
ws_new['A1'].font = TITLE_FONT
ws_new['A1'].alignment = Alignment(horizontal='center', vertical='center')
ws_new.row_dimensions[1].height = 30

# 表头
headers = ['序号', '工程项目或费用名称', '单位', '总数量', '单价（元）', '合计（元）']
for col, h in enumerate(headers, 1):
    cell = ws_new.cell(row=3, column=col, value=h)
    cell.font = HEADER_FONT
    cell.fill = HEADER_FILL
    cell.alignment = Alignment(horizontal='center', vertical='center')
    cell.border = THIN_BORDER

ws_new.row_dimensions[3].height = 22

# 数据行
row_idx = 4
seq = 1
grand_total = 0

for name, info in projects.items():
    ws_new.cell(row=row_idx, column=1, value=seq).border = THIN_BORDER
    ws_new.cell(row=row_idx, column=2, value=name).border = THIN_BORDER
    ws_new.cell(row=row_idx, column=3, value=info['unit']).border = THIN_BORDER

    qty_cell = ws_new.cell(row=row_idx, column=4)
    qty_cell.value = info['total_qty']
    qty_cell.border = THIN_BORDER
    qty_cell.number_format = '0.##'

    price_cell = ws_new.cell(row=row_idx, column=5)
    price_cell.value = info['price']
    price_cell.border = THIN_BORDER
    price_cell.number_format = '#,##0'

    total_cell = ws_new.cell(row=row_idx, column=6)
    total_cell.value = info['total_amount']
    total_cell.border = THIN_BORDER
    total_cell.number_format = '#,##0.00'

    # 斑马纹
    fill = ZEBRA_FILL_1 if seq % 2 == 1 else ZEBRA_FILL_2
    for c in range(1, 7):
        ws_new.cell(row=row_idx, column=c).fill = fill

    grand_total += info['total_amount']
    seq += 1
    row_idx += 1

# 合计行
ws_new.cell(row=row_idx, column=1, value='').border = THIN_BORDER
ws_new.merge_cells(start_row=row_idx, start_column=1, end_row=row_idx, end_column=5)
total_label = ws_new.cell(row=row_idx, column=1, value='合计')
total_label.font = TOTAL_FONT
total_label.fill = TOTAL_FILL
total_label.alignment = Alignment(horizontal='right', vertical='center')
total_label.border = THIN_BORDER
for c in range(2, 6):
    ws_new.cell(row=row_idx, column=c).fill = TOTAL_FILL
    ws_new.cell(row=row_idx, column=c).border = THIN_BORDER

total_val = ws_new.cell(row=row_idx, column=6)
total_val.value = grand_total
total_val.font = TOTAL_FONT
total_val.fill = TOTAL_FILL
total_val.border = THIN_BORDER
total_val.number_format = '#,##0.00'

ws_new.row_dimensions[row_idx].height = 24

# 列宽
ws_new.column_dimensions['A'].width = 6
ws_new.column_dimensions['B'].width = 40
ws_new.column_dimensions['C'].width = 8
ws_new.column_dimensions['D'].width = 12
ws_new.column_dimensions['E'].width = 12
ws_new.column_dimensions['F'].width = 14

output_path = '/Users/wencong/Documents/房/home/04-报价/百艺/基础最新报价_按项目合并.xlsx'
wb_new.save(output_path)
print(f'已生成: {output_path}')
print(f'合并后共 {seq-1} 个项目')
print(f'总金额: {grand_total:.2f} 元')
