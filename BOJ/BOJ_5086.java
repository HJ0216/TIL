import java.util.Scanner;

public class Main {
	public static void main(String[] args) {
		Scanner scan = new Scanner(System.in);

		while(true) {
			int x1 = scan.nextInt();
			int y1 = scan.nextInt();
		
			if(x1==0 && y1==0) {break;}
			
			if((y1 % x1)==0) {System.out.println("factor");}
			else if((x1 % y1)==0) {System.out.println("multiple");}
			else {System.out.println("neither");}
		
		}
		
		scan.close();

	}
}
