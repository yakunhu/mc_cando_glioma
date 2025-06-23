import random

original='/projects/academic/rams/sumeixu/rd_ecfp4-int-dice-alphafold-homo_sapien-coach-c0.0-p0.0-CxP-approved.tsv'
new_name = "random control1"
def scramble_matrix(original, new_name):
  with open(original, 'r') as f:
    lines = f.read().strip().split('\n')

  out_lines = []
  for line in lines:
    cells = line.split('\t')
    label, contents = cells[0], cells[1:]
    for _ in range(5):
      random.shuffle(contents)
    out_lines.append(label + '\t' + '\t'.join(contents) + '\n')

  with open(new_name, 'w') as f:
    f.writelines(out_lines)

scramble_matrix(original, new_name)


