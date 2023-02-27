import java.util.Scanner;

public class Main {
	public static void main(String[] args) {
		Scanner scan = new Scanner(System.in);
		int input = scan.nextInt();
		
		int a=1;
		
		for(int n=0; ; n++) {
			if(input<=(a+=6*n)) {
				System.out.println(n+1);
				break;
			} // if
		} // for
		
		scan.close();
	}
}
