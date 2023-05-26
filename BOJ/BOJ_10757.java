import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.math.BigInteger;
import java.util.StringTokenizer;

public class Main {
	public static void main(String[] args) throws Exception {
			BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
			BufferedWriter bw = new BufferedWriter(new OutputStreamWriter(System.out));
	
			StringTokenizer st = new StringTokenizer(br.readLine());
			BigInteger bigInt1 = new BigInteger(st.nextToken());
			BigInteger bigInt2 = new BigInteger(st.nextToken());

			bw.write(bigInt1.add(bigInt2) + "");
			
			bw.flush();
			bw.close();
			
	}
}
