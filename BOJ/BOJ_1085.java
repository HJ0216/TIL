import java.util.Scanner;

public class Main {
	public static void main(String[] args) {
		Scanner scan = new Scanner(System.in);
		int a = scan.nextInt();
		int b = scan.nextInt();
		int x = scan.nextInt();
		int y = scan.nextInt();
		
		if(2*a>=x) {
			if(2*b>=y) {
				if(x-a>=y-b) {System.out.println(y-b);}
				else {System.out.println(x-a);}
			} else {
				if(x-a>=b) {System.out.println(b);}
				else {System.out.println(x-a);}				
			}
		} else {
			if(2*b>=y) {
				if(a>=y-b) {System.out.println(y-b);}
				else {System.out.println(a);}
			} else {
				if(a>=b) {System.out.println(b);}
				else {System.out.println(a);}
			}
		}
		
		scan.close();
	}
}
