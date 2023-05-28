import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;

public class Main {
	public static void main(String[] args) throws Exception {

		BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
		BufferedWriter bw = new BufferedWriter(new OutputStreamWriter(System.out));

		int a1 = Integer.parseInt(br.readLine());
		int a2 = Integer.parseInt(br.readLine());
		int a3 = Integer.parseInt(br.readLine());
		
		if((a1 + a2 + a3)== 180) {
			if(a1 == a2 && a2 == a3) {
				bw.write("Equilateral\n");
			} else if((a1!=a2)&&(a1!=a3)&&(a2!=a3)) {
				bw.write("Scalene\n");				
			} else {
				bw.write("Isosceles\n");				
			}
		} else {
			bw.write("Error\n");
		}
		
		bw.flush();
		bw.close();

	}
}
