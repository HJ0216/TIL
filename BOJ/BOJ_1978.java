import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.util.StringTokenizer;

public class Main {

	public static void main(String[] args) throws IOException {
		BufferedWriter bw = new BufferedWriter(new OutputStreamWriter(System.out));
		BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
		
		int cnt = Integer.parseInt(br.readLine());
		StringTokenizer st = new StringTokenizer(br.readLine(), " ");

		int cntPrime=0;
		while(st.hasMoreTokens()) {
			int chk = Integer.parseInt(st.nextToken());
			if(chk!=1 && isPrime(chk)) {
				cntPrime++;
			}
		}

		bw.write(cntPrime + "");
		
		bw.flush();
		bw.close();
		
	}
	
	public static boolean isPrime(int number) {
		for(int i=2; i<number; i++) {
			if(number%i==0) {
				return false;
			}
		}
		return true;
	}
	
}
