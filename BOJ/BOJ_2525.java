import java.util.Scanner;

public class Main {
	public static void main(String[] args) {
		
		Scanner scan = new Scanner(System.in);
		int h = scan.nextInt();
		int m = scan.nextInt();
		int a = scan.nextInt();

		int min = m+a;
		
		while(true) {
			if(min>=60) {
				min -= 60;
				h += 1;
			} else {
				break;				
			}
		}
		
		while(true) {
			if(h>=24) {
				h -= 24;
			} else {
				break;				
			}
		}
		
		System.out.println(h + " " + min);
		
		scan.close();
	}
}
