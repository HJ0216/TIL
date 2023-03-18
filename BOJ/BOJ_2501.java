import java.util.ArrayList;
import java.util.Scanner;

public class Main {
	public static void main(String[] args) {
		Scanner scan = new Scanner(System.in);
		int a = scan.nextInt();
		int b = scan.nextInt();
		
		ArrayList<Integer> arrList = new ArrayList<>();
		
		for(int i=1; i<=a; i++) {
			if(a%i==0) {
				arrList.add(i);
			}
		}
		
		try {
			System.out.println(arrList.get(b-1));
		} catch(IndexOutOfBoundsException e){
			System.out.println(0);
		}
		
		scan.close();
	}
}
