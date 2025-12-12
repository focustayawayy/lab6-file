class Node:
    def __init__(self, name, priority):
        self.name = name
        self.priority = priority  
        self.next = None


class PatientQueue:
    def __init__(self):
        self.head = None

    def add_patient(self, name, priority):
        new_node = Node(name, priority)
        if self.head is None or priority < self.head.priority:
            new_node.next = self.head
            self.head = new_node
            return

        current = self.head
        while current.next and current.next.priority <= priority:
            current = current.next

        new_node.next = current.next
        current.next = new_node

    def process_patient(self):
        if self.head is None:
            return None

        patient = self.head
        self.head = self.head.next
        return patient.name, patient.priority

    def show_queue(self):
        current = self.head
        if current is None:
            print("The queue is empty.")
            return

        print("Patient queue (sorted by priority):")
        while current:
            print(f"{current.name} — priority {current.priority}")
            current = current.next


def main():
    queue = PatientQueue()

    while True:
        print("\n1 — Add patient")
        print("2 — Process next patient")
        print("3 — Show all patients")
        print("4 — Exit")

        choice = input("Choose: ")

        if choice == "1":
            name = input("Enter patient name: ")
            priority = int(input("Enter priority (1 = severe case): "))
            queue.add_patient(name, priority)
            print("Patient added.")

        elif choice == "2":
            result = queue.process_patient()
            if result:
                print(f"Processed: {result[0]} (priority {result[1]})")
            else:
                print("Queue is empty.")

        elif choice == "3":
            queue.show_queue()

        elif choice == "4":
            print("Exiting program...")
            break

        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    main()
