from http import client
import sympy as smp
import operator as op

ops = {
    '+' : op.add,
    '*' : op.mul,
    '|' : op.or_,
    '&' : op.and_
}

# Класс сотрудника
class Employee:
    def __init__(self):
        self.self_confidence = int(input("Уверены ли Вы в корректности общения с клиентом? (1 - да / 2 - нет): "))
        self.emp_emotional_state = int(input("Какое у Вас на данный момент эмоциональное состояние? (жизнерадостное - 1/раздражительное - 2): "))
        self.communication_type = int(input("Диалог проходит дружелюбно? (1 - да / 2 - нет): "))
        self.client_correctness = int(input("Уверены ли Вы, что правильно понимаете клиента? (1 - да, 2 - нет): "))
        self.feelings = int(input("Ухудшается ли Ваше эмоциональное состояние при общении с клиентом? (1 - да, 2 - нет): "))
        self.vision_of_client = int(input("Как Вы считаете негативно или дружелюбно настроен клиент? (1 - негативно, 2 - дружелюбно): "))
        self.user_type = True

    def prepare_a(self):
        if self.communication_type == 2:
            if self.emp_emotional_state == 2:
                self.user_type = False
            elif self.emp_emotional_state == 1:
                self.user_type = True
        elif self.communication_type == 1:
            if self.emp_emotional_state == 1:
                self.user_type == True
            elif self.emp_emotional_state == 2:
                self.user_type == True
        return self.user_type

# Класс клиента
class Client:
    def __init__(self):
        self.cl_emotional_state = int(input("Как Вы себя чувствуете? (1 - позитивно, 2 - негативно): "))
        self.communication_type = int(input("Какой диалог Вы желаете вести с сотрудником? (1 - позитивный, 2 - негативный): "))
        self.communication_confidence = int(input("Уверены ли Вы, что правильно общаетесь с сотрудником? (1 - да, 2 - нет): "))
        self.blame_employee = int(input("Вините ли Вы сотрудника в своей проблеме? (1 - да, 2 - нет): "))
        self.client_type = True

    def prepare_b(self):
        if self.communication_type == 1:
            if self.cl_emotional_state == 1:
                self.client_type = True
            elif self.cl_emotional_state == 2:
                self.client_type = False
        elif self.communication_type == 2:
            if self.cl_emotional_state == 1:
                self.client_type = False
            elif self.cl_emotional_state == 2:
                self.client_type = False
        return self.client_type

            
# Класс взаимодействие (составление формулы)
class Communication:
    def __init__(self, employee: Employee, client: Client):
        self.employee = employee
        self.client = client
        self.a_exp_a = True
        self.a_exp_b = True
        self.a_exp_comm = "&"
        self.b_exp_a = True
        self.b_exp_b = True
        self.b_exp_comm = True
        self.a_corr_a = True
        self.a_corr_b = True
        self.a_corr_comm = "&"
        self.b_corr_a = True
        self.b_corr_b = True
        self.b_corr_comm = True
        self.a = employee.user_type
        self.b = client.client_type
        self.communication = "&"
        self.employee = employee
        self.client = client
        self.emp_message = ""
        self.cl_message = ""

        
    def make_communication(self):
        # Видение сотрудника (индивида a)
        if self.employee.self_confidence == False:
            self.a_corr_a = False
        if self.employee.vision_of_client == 1:
            self.a_exp_b = False
        elif self.employee.vision_of_client == 2:
            self.a_exp_b = True
        if self.employee.client_correctness == 2:
            self.a_corr_b = False
        # Видение клиента (индивида b)
        if self.client.communication_confidence == 1:
            self.b_corr_b = True
        elif self.client.communication_confidence == 2:
            self.b_corr_b = False
        if self.client.blame_employee == 1:
            self.b_corr_a = False
        elif self.client.blame_employee == 2:
            self.b_corr_a = True
        if self.client.communication_type == 1:
            self.b_corr_comm = "&"
            self.b_exp_comm = "&"
        elif self.client.communication_type == 2:
            self.b_corr_comm = "|"
            self.b_exp_comm = "|"
        
        # Обозначение переменных    
        a_f, b_f, a_exp_a_f, a_exp_b_f, \
        a_corr_a_f, a_corr_b_f, b_exp_a_f, \
        b_exp_b_f, b_corr_a_f, b_corr_b_f = smp.symbols('a_f,b_f,a_exp_a_f,a_exp_b_f,a_corr_a_f,a_corr_b_f,b_exp_a_f,b_exp_b_f,b_corr_a_f,b_corr_b_f')
        # Построение выражения для сотрудника
        if self.a_corr_comm == "&" and self.a_exp_comm == "&":
            a_formula = a_f | (~(a_exp_a_f | (~(a_corr_a_f & a_corr_b_f)) & a_exp_b_f))
        elif self.a_corr_comm == "|" and self.a_exp_comm == "|":
            a_formula = a_f | (~(a_exp_a_f | (~(a_corr_a_f | a_corr_b_f)) | a_exp_b_f))
        # Построение выражения для клиента
        if self.b_corr_comm == "&" and self.b_exp_comm == "&":
            b_formula = b_f | (~(b_exp_a_f & b_exp_b_f | (~(b_corr_a_f & b_corr_b_f))))
        elif self.b_corr_comm == "|" and self.b_exp_comm == "|":
            b_formula = b_f | (~(b_exp_a_f | b_exp_b_f | (~(b_corr_a_f | b_corr_b_f))))
        
        # Составление формулы взаимодействия
        formula = (a_formula & b_formula).subs({a_f: self.a, a_exp_a_f: self.a_exp_a, a_corr_a_f: self.a_corr_a,
                                                a_corr_b_f: self.a_corr_b, a_exp_b_f: self.a_exp_b,
                                                b_f: self.b, b_exp_a_f: self.b_exp_a,
                                                 b_exp_b_f: self.b_exp_b, b_corr_a_f: self.b_corr_a,
                                                 b_corr_b_f: self.b_corr_b})

        return formula

    def show_employee_description(self):
        if self.employee.self_confidence == 1 and self.employee.emp_emotional_state == 1:
            print("Сотрудник - позитивный настрой (1), не сомневается в своих действиях")
        elif self.employee.self_confidence == 1 and self.employee.emp_emotional_state == 2:
            print("Сотрудник - негативный настрой (0), не сомневается в своих действиях")
        elif self.employee.self_confidence == 2 and self.employee.emp_emotional_state == 2:
            print("Сотрудник - негативный настрой (0), сомневается в своих действиях")
        elif self.employee.self_confidence == 2 and self.employee.emp_emotional_state == 1:
            print("Сотрудник - позитивный настрой (1), сомневается в своих действиях")

        if self.employee.client_correctness == 1:
            print("Сотрудник уверен в своём видении клиента")
        elif self.employee.client_correctness == 2:
            print("Сотрудник не уверен в совём видении клиента")

        if self.employee.vision_of_client == 1:
            print("Сотрудник видит клиента негативным")
        elif self.employee.vision_of_client == 2:
            print("Сотрудник видит клиента позитивным")

        if self.employee.communication_type == 1:
            print("Сотрудник понимает взаимодействие с клиентом как союз\n\n")
        elif self.employee.communication_type == 2:
            print("Сотрудник понимает взаимодействие с клиентом как конфронтацию\n\n")

    def show_client_description(self):
        if self.client.cl_emotional_state == 1 and self.client.communication_confidence == 1:
            print("Клиент - позитивный настрой (1), не сомневается в своих действиях")
        elif self.client.cl_emotional_state == 2 and self.client.communication_confidence == 1:
            print("Клиент - негативный настрой (0), не сомневается в своих действиях")
        elif self.client.cl_emotional_state == 1 and self.client.communication_confidence == 2:
            print("Клиент - позитивный настрой (1), сомневается в своих действиях")
        elif self.client.cl_emotional_state == 2 and self.client.communication_confidence == 2:
            print("Клиент - негативный настрой (0), сомневается в своих действиях")
        
        if self.client.blame_employee == 1:
            print("Клиент видит сотрудника негативным")
        elif self.client.blame_employee == 2:
            print("Клиент видит сотрудника позитивным")

        if self.client.communication_type == 1:
            print("Клиент понимает взаимодействие с сотрудником как союз\n\n")
        elif self.client.communication_type == 2:
            print("Клиент понимает взаимодействие с сотрудником как конфронтацию\n\n")
    
    def give_advice_for_employee(self, formula):
        print("Совет для сотрудника:")
        if formula == False:
            if self.employee.emp_emotional_state == 2 and self.client.cl_emotional_state == 1:
                self.emp_message = "Ваша задача помочь клиенту, он настроен положительно, можете чувствовать себя спокойно"
            elif self.employee.self_confidence == 2 and self.employee.client_correctness == 1:
                if self.employee.feelings == 1 and self.employee.vision_of_client == 1:
                    self.emp_message = "В негативном общении с клиентом нет Вашей вины, держитесь спокойно"
            elif self.employee.self_confidence == 2 and self.employee.client_correctness == 2:
                self.emp_message == "Будьте уверены в своих действиях. Вы пытаетесь помочь клиенту и сделать этот мир лучше :)"
            elif (self.employee.feelings == 1 and self.client.blame_employee == 1) or (self.employee.feelings == 2 and self.client.blame_employee == 1):
                print("Клиент не понимает, что Вы не виноваты в его проблеме. Не принимайте его высказывания близко к сердцу. Вы ему помогаете и не виновны в его проблеме.")
            

        if formula == True:
            self.emp_message = "Диалог проходит в позитивном ключе, спасибо за работу!"

        print(self.emp_message)
    

    def give_advice_for_client(self, formula):
        print("Совет для клиента:")
        if self.client.communication_type == 2:
            self.cl_message = "Клиент старается всеми силами Вам помочь. Пожалуйста, ведите коммуникацию уважительно :)"
        if formula == True:
            self.cl_message = "Спасибо, что обратились в поддержку"
        if formula == False:
            if self.client.blame_employee == 1:
                self.cl_message = "Сотрудник будет рад помочь Вам. Пожалуйста, будьте вежливы"
            if self.client.communication_confidence == 2:
                self.cl_message = "Клиент старается всеми силами Вам помочь. Пожалуйста, ведите коммуникацию уважительно :)"
            if self.client.cl_emotional_state == 2:
                self.cl_message = "Мы рады, что Вы обратились в поддержку и приложим все усилия для того, чтобы помочь"
        print(self.cl_message)


# Запуск прототипа
if __name__ == '__main__':
    # Выбор для имитации роли
    answer = int(input("Выберите роль: 1 - сотрудник, 2 - клиент: "))
    if answer == 1:
        employee1 = Employee()
        employee1.prepare_a()
        print("Переход на роль клиента\n")
        client1 = Client()
        client1.prepare_b()
    elif answer == 2:
        client1 = Client()
        client1.prepare_b()
        print("Переход на роль сотрудника\n")
        employee1 = Employee()
        employee1.prepare_a()

    # Создание объекта коммуникации
    communication = Communication(employee1, client1)
    # Показать описание сотрудника и клиента
    communication.show_employee_description()
    communication.show_client_description()
    # Вывод результата формулы
    print(communication.make_communication())
    result = communication.make_communication()

    # Вывод советов для сотрудника и клиента
    communication.give_advice_for_employee(result)
    communication.give_advice_for_client(result)
