using System;
using System.Collections.Generic;
using System.Linq;
using System.Text.RegularExpressions;
// using MathNet.Numerics;

namespace Soale2
{
    
    class PDAStack
    {
        Stack<string> stack;
        public PDAStack()
        {
            stack = new Stack<string>();
        }
        public int count()
        {return stack.Count;}
        public string pop()                  
        {
            if (stack.Count != 0)
            {
                string p = stack.Pop();
                return p;
            }
            else
                return "$";
        }
                            
        public string top()         
        {    
            if (stack.Count != 0)
                return stack.Peek();
            else
                return "$";
        }

        public void push(string s)   
        {
            stack.Push(s);
        }
    }
    class PDA
    {
        public PDAStack stack;
        public PDAStack grammarStack;
        public string Infix;
        public string Postfix;
        public PDA(string s)
        {
            stack = new PDAStack();
            grammarStack = new PDAStack();
            var reg = new Regex(@"[0-9]\s[0-9]");
            // var reg2 = new Regex(@"[\][\]");
            if (reg.IsMatch(s) || s.Contains("()") || s.Contains("//") || s.StartsWith("*") || s.StartsWith("/"))
                throw new FormatException();
            Infix = s.ToLower().Replace(" ", "");
            Postfix = BuildPostfix();
        }
        public static bool IsVarOrNum(char c)
        {return char.IsNumber(c) || c == '.';}
        public static int Priority(string c)
        {
            switch(c)
            {
                case "^" : return 4;
                case "sqrt" : return 3;
                case "sin" : return 3;
                case "cos": return 3;                                           
                case "tan"  : return 3;
                case "asin" : return 3;
                case "acos" : return 3;
                case "atan" : return 3;
                case "sgn" : return 3;
                case "abs" : return 3;
                case "exp" : return 3;
                case "ln" : return 3;
                case "sinh" : return 3;
                case "cosh" : return 3;
                case "tanh" : return 3;
                case "/" : return 2;
                case "*": return 2;                                           
                case "+"  : return 1;
                case "-" : return 1;
                default  : return 0;
            }
        }
        public static double Operate(char o, string d1, string d2)
        {
            double b = double.Parse(d1);
            double a = double.Parse(d2);
            switch(o)
            {
                case '^' : return Math.Pow(a, b);
                case '/' : return a/b;
                case '*': return a*b;                                           
                case '+'  : return a+b;
                case '-' : return a-b;
                default  : return 0;
            }
        }
        private double OperateFunc(string ss, string v)
        {
            double a = double.Parse(v);
            switch(ss)
            {
                case "sqrt" : return Math.Sqrt(a);
                case "sin" : return Math.Sin(a);
                case "cos": return Math.Cos(a);                                           
                case "tan"  : return Math.Tan(a);
                case "asin" : return Math.Asin(a);
                case "acos" : return Math.Acos(a);
                case "atan" : return Math.Atan(a);
                case "sgn" : return Math.Sign(a);
                case "abs" : return Math.Abs(a);
                case "exp" : return Math.Exp(a);
                case "ln" : return Math.Log(a, Math.E);
                case "sinh" : return Math.Sinh(a);
                case "cosh" : return Math.Cosh(a);
                case "tanh" : return Math.Tanh(a);
                default  : return 0;
            }
        }
        public string BuildPostfix()
        {
            string p;
            string postfix = "";
            for(int i=0 ; i < Infix.Length; i++)
            {
                if(IsVarOrNum(Infix[i]) || (i != 0 && (Infix.Substring(i-1, 2) == "^-" || Infix.Substring(i-1, 2) == "(-" || Infix.Substring(i-1, 2) == "*-" || Infix.Substring(i-1, 2) == "/-")))   
                {
                    string ss = $"({Infix[i]}";
                    while (++i != Infix.Length && IsDigit(Infix[i]))
                        ss += Infix[i];
                    postfix += ss+')';
                    i--; 
                }
                else if(Infix[i]=='(')
                {
                    postfix += Infix[i];
                    stack.push(Infix[i].ToString());
                    grammarStack.push("(");
                }
                else if(Infix[i]==')')
                {
                    var last = grammarStack.pop();
                    if(last != "(")
                        throw new FormatException();
                    postfix += Infix[i];
                    while((p = stack.pop()) != "(")
                    {
                        if(p == "$") 
                            throw new FormatException();
                        postfix += p;
                    }
                }
                else if(char.IsLetter(Infix[i]))
                {
                    string ss = $"{Infix[i]}";
                    while (++i != Infix.Length && char.IsLetter(Infix[i]) && (Priority(ss) == 0 || Infix[i+1] =='h' || Infix[i] =='h'))
                        ss += Infix[i];
                    while(Priority(ss) <= Priority((p = stack.top()).ToString()) && stack.top() != "$")
                        postfix += stack.pop();
                    // postfix += ss;
                    i--;
                    stack.push(ss);    
                }
                else if (Priority(Infix[i].ToString()) != 0)
                {
                    while(Priority(Infix[i].ToString()) <= Priority((p = stack.top()).ToString()) && stack.top() != "$")
                        postfix += stack.pop();
                    stack.push(Infix[i].ToString());    
                }
            }
            if(grammarStack.count()!= 0)  throw new FormatException();
            while((p = stack.pop()) != "$")
                postfix += p;
            return postfix;
        }
        public double ComputeFunc()
        {
            string s = Postfix;
            for (int j = 0; j < s.Length; j++) 
            { 
                if(j == s.Length - 1 && char.IsLetter(s[j])) break;
                if(char.IsNumber(s[j]) || (j != 0 && s.Substring(j-1, 2) == "(-"))
                {
                    string ss = s[j].ToString();
                    while (IsDigit(s[++j]))
                        ss += s[j];
                    stack.push(ss);
                    j--;
                }
                else if(char.IsLetter(s[j]))
                {
                    string ss = s[j].ToString();
                    while (j != s.Length -1 && char.IsLetter(s[++j]) && Priority(ss) == 0)
                        ss += s[j];
                    // stack.push(ss);
                    j--;
                    if (Priority(ss) != 0)
                    {
                        var rr = OperateFunc(ss, stack.pop()).ToString();
                        if(rr == "NaN" || rr == "-∞" || rr == "∞" || rr == "Infinity" || rr == "-Infinity") 
                            throw new FormatException();
                        stack.push(rr);
                    }
                }
                else if (Priority(s[j].ToString()) != 0)
                {
                    var rr = Operate(s[j], stack.pop(), new string[]{"$","^"}.Contains(stack.top())?"0":stack.pop()).ToString();
                    if(rr == "NaN" || rr == "-∞" || rr == "∞" || rr == "$" || rr == "Infinity" || rr == "-Infinity") 
                            throw new FormatException();
                    stack.push(rr);
                }
                    
            } 
            var result = stack.pop();
            if(result == "NaN" || result == "-∞" || result == "∞" || result == "$" || result == "Infinity" || result == "-Infinity") 
                throw new FormatException();
            return double.Parse(result);
        }

        private bool IsDigit(char v)
        {return char.IsNumber(v) || v == '.';}
    }
    class Program
    {
        static void Main(string[] args)
        {
            string result;
            try
            {
                var pda = new PDA(Console.ReadLine());

                // result = (pda.ComputeFunc() - (pda.ComputeFunc() % 0.01)).ToString().Replace(",", "");
                var r = pda.ComputeFunc();
                if(r%0.1 >= 0.09999)
                    r = Math.Round(r, 2);
                result = (Math.Truncate(r *100)/100).ToString("0.00").Replace(",", "");
                System.Console.Write(result);
            }
            catch
            {
                Console.WriteLine("INVALID");
            }
        }
    }
}
