import sys

class TuringMachine:
    def __init__(self, input_string):
       
        self.tape = list(input_string) + ['_']
   
        self.head_position = 0
        
        
        self.current_state = 'q0'
        
    
        self.accept_state = 'q7'  
        self.reject_state = 'q_red'
        
        self.is_halted = False  
        
 
        self.digits = set('0123456789')
        self.uppercase_letters = set('ABCDEFGHIJKLMNOPQRSTUVWXYZ')

    def print_step(self, read_symbol, move):
        """Her adımda mevcut durumu, okunan sembolü, kafa hareketini ve dinamik bant içeriğini yan yana gösterir."""
     
        display_symbol = "boşluk" if read_symbol == '_' else read_symbol
        
       
        visual_tape = []
        for i, char in enumerate(self.tape):
            if i == self.head_position:
               
                tape_char = "_" if char == '_' else char
                visual_tape.append(f"[{tape_char}]")
            else:
                tape_char = "_" if char == '_' else char
                visual_tape.append(tape_char)
        
        tape_str = "".join(visual_tape)
        
        
        print(f"Mevcut Durum: {self.current_state:<5} | Okunan Sembol: {display_symbol:<6} | Kafa Hareketi: {move:<8} | Bant İçeriği: {tape_str}")

    def step(self):
        """Turing makinesinin geçiş fonksiyonunu (transition function) işletir."""
        if self.head_position < 0 or self.head_position >= len(self.tape):
            read_symbol = '_'
        else:
            read_symbol = self.tape[self.head_position]

        if self.current_state == 'q0':
            if read_symbol in self.digits:
                self.print_step(read_symbol, "Sağ (R)")
                self.current_state = 'q1'
                self.head_position += 1
            else:
                self.print_step(read_symbol, "Dur (S)")
                self.current_state = self.reject_state

      
        elif self.current_state == 'q1':
            if read_symbol in self.digits:
                self.print_step(read_symbol, "Sağ (R)")
                self.current_state = 'q2'
                self.head_position += 1
            else:
                self.print_step(read_symbol, "Dur (S)")
                self.current_state = self.reject_state

        #
        elif self.current_state == 'q2':
            if read_symbol in self.uppercase_letters:
                self.print_step(read_symbol, "Sağ (R)")
                self.current_state = 'q3'
                self.head_position += 1
            else:
                self.print_step(read_symbol, "Dur (S)")
                self.current_state = self.reject_state

      
        elif self.current_state == 'q3':
            if read_symbol in self.uppercase_letters:
                self.print_step(read_symbol, "Sağ (R)")
                self.current_state = 'q4'
                self.head_position += 1
            else:
                self.print_step(read_symbol, "Dur (S)")
                self.current_state = self.reject_state

        elif self.current_state == 'q4':
            if read_symbol in self.digits:
                self.print_step(read_symbol, "Sağ (R)")
                self.current_state = 'q5'
                self.head_position += 1
            else:
                self.print_step(read_symbol, "Dur (S)")
                self.current_state = self.reject_state

      
        elif self.current_state == 'q5':
            if read_symbol in self.digits:
                self.print_step(read_symbol, "Sağ (R)")
                self.current_state = 'q6'
                self.head_position += 1
            else:
                self.print_step(read_symbol, "Dur (S)")
                self.current_state = self.reject_state

   
        elif self.current_state == 'q6':
            if read_symbol in self.digits:
                self.print_step(read_symbol, "Sağ (R)")
                self.current_state = 'q7'
                self.head_position += 1
            else:
                self.print_step(read_symbol, "Dur (S)")
                self.current_state = self.reject_state

        elif self.current_state == 'q7':
            if read_symbol == '_':
                self.print_step(read_symbol, "Dur (S)")
                self.is_halted = True 
            else:
                self.print_step(read_symbol, "Dur (S)")
                self.current_state = self.reject_state

 
        elif self.current_state == 'q_red':
            self.is_halted = True

    def run(self):
        """Simülasyonu başlatır ve sonuç üretir."""
        print(f"\nBanta yerleştirildi: {''.join(self.tape)}\n")
        
        while not self.is_halted:
            self.step()

        print("-" * 80)
        if self.current_state == 'q7':
            print("Sonuç: KABUL")
            print("Plaka formatı GEÇERLİ.")
            return "KABUL"
        else:
            print("Sonuç: RED")
            print("Plaka formatı GEÇERSİZ!")
            return "RED"



if __name__ == "__main__":
    print("-----------------------------------------------")
    
    print("TURING MAKİNESİ İLE ARAÇ PLAKA FORMATI TANIYICI")
    print("-----------------------------------------------")
   
    
    user_input = input("Lütfen kontrol edilecek plakayı giriniz: ")
    
    if not user_input.strip():
        print("\nHata: Boş bir değer giremezsiniz!")
    else:
        tm = TuringMachine(user_input)
        tm.run()
