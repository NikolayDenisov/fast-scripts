### Обзор классов на python
```
class FirstClass:           # Определяет объект класса
  def setdata(self, value): # Определяет метод класса
    self.data = value       # self – это экземпляр
  
  def display(self):
    print(self.data)        # self.data: данные экземпляров
```

```
x = FirstClass() # Создаются два экземпляра
y = FirstClass() # Каждый является отдельным пространством имен
```
```
x.setdata(“King Arthur”) #Вызов метода : self – это x
y.setdata(3.14159)       #Эквивалентно: FirstClass.setdata(y, 3.14159)
```
``` 
x.display() # В каждом экземпляре свое значение self.data
King Arthur 
y.display()
3.1415
```
