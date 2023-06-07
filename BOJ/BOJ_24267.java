import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.math.BigInteger;

public class Main {
	public static void main(String[] args) throws Exception {

		BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
		BufferedWriter bw = new BufferedWriter(new OutputStreamWriter(System.out));

		int n = Integer.parseInt(br.readLine());

		BigInteger sum = BigInteger.ZERO;

		for (int i = n - 2; i > 0; i--) {
		    BigInteger iBigInteger = BigInteger.valueOf(i);
		    sum = sum.add(iBigInteger.multiply(iBigInteger.add(BigInteger.ONE)).divide(BigInteger.TWO));
		}

		bw.write(sum.toString() + "\n" + 3);
		bw.flush();
		}
}
