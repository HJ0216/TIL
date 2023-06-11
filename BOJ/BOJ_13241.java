import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.util.StringTokenizer;

public class Main {
	public static void main(String[] args) throws Exception {

		BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
		BufferedWriter bw = new BufferedWriter(new OutputStreamWriter(System.out));

		StringTokenizer st = new StringTokenizer(br.readLine(), " ");
		int a = Integer.parseInt(st.nextToken());
		long b = Long.parseLong(st.nextToken());
		
		long max = 0;
		
		for(int i=1; i<=1000; i++) {
			if(a % i ==0 && b % i == 0) {
				max = Math.max(max, i);
			}
		}

		long result = (a/max) * (b/max) * max;

		bw.write(result+"");
		bw.flush();
	}
}
