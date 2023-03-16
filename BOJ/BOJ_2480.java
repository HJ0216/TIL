import java.util.Scanner;

public class Main {
	public static void main(String[] args) {
		Scanner scan = new Scanner(System.in);
		int a1 = scan.nextInt();
		int a2 = scan.nextInt();
		int a3 = scan.nextInt();
		
		if(a1==a2) {
			if(a2==a3) {System.out.println(10000+1000*a1);}
			else {System.out.println(1000+100*a1);}
		} else if(a1==a3) {
			if(a3==a2) {System.out.println(10000+1000*a1);}
			else {System.out.println(1000+100*a1);}
		} else if(a2==a3) {
			if(a3==a1) {System.out.println(10000+1000*a1);}
			else {System.out.println(1000+100*a2);}			
		} else {
			int max = Math.max(a1, a2);
			max = Math.max(max, a3);
			System.out.println(max*100);
		}
	}
}
