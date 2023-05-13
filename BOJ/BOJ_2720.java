import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;

public class Main {
	public static void main(String[] args) throws Exception {
		BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
		BufferedWriter bw = new BufferedWriter(new OutputStreamWriter(System.out));

		int totalNum = Integer.parseInt(br.readLine());
		for(int i=0; i<totalNum; i++) {
			int test = Integer.parseInt(br.readLine());
			bw.write(test/25 + " ");
			test = test%25;
			bw.write(test/10 + " ");
			test = test%10;
			bw.write(test/5 + " ");
			test = test%5;
			bw.write(test + "\n");
		}

		bw.flush();
		bw.close();
		
	}
}
