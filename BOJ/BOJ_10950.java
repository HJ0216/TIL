import java.util.ArrayList;
import java.util.Scanner;

public class Main {
	public static void main(String[] args) {
		Scanner scan = new Scanner(System.in);
		int a = scan.nextInt();

		ArrayList<Integer> arrList = new ArrayList<>();
		
		for(int i=0; i<a*2; i++) {
			arrList.add(scan.nextInt());
		}

		for(int i=0; i<a*2; i+=2) {
			System.out.println(arrList.get(i)+arrList.get(i+1));
		}
		
		scan.close();
	}
}
