import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;

public class Main {
	public static void main(String[] args) throws Exception {

		BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
		BufferedWriter bw = new BufferedWriter(new OutputStreamWriter(System.out));

		int totalDot = Integer.parseInt(br.readLine());
		
		int total = 2;
		int mul = 0;
		for(int i=0; i<totalDot; i++) {
			total = total + (total-1);
			mul = total*total;
		}
		bw.write(mul + "");
		
		bw.flush();
		bw.close();

	}
}
