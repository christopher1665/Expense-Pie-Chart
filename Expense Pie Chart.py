import matplotlib.pyplot as plt
def main():
    infile = open('expenses.txt', 'r')
    slice_labels = []
    while '' not in slice_labels:
        slice_labels.append(infile.readline().rstrip('=0123456789\n'))
    slice_labels.remove('')

    infile = open('expenses.txt', 'r')
    bills = []
    while '' not in bills:
        bills.append(infile.readline().lstrip('qwertyuiopasdfghjklzxcvbnm =').rstrip('\n'))
    bills.remove('')

    infile.close()
    plt.pie(bills, labels=slice_labels)
    plt.title('Bills')
    plt.show()

if __name__ == '__main__':
    main()