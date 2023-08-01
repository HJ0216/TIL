import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;

public class Main {

	public static void main(String[] args) throws IOException {
		BufferedReader br = new BufferedReader(new InputStreamReader(System.in));

		int min = Integer.parseInt(br.readLine());
		int max = Integer.parseInt(br.readLine());

		if(min==1) {
			calPrimeNum(min+1, max);
		} else {
			calPrimeNum(min, max);	
		}
		
	}

	public static void calPrimeNum(int min, int max) throws IOException {

		BufferedWriter bw = new BufferedWriter(new OutputStreamWriter(System.out));

		boolean[] bArr = new boolean[10001];

		for (int i = min; i <= max; i++) {
			for (int j = 2; j < i; j++) {
				if (i % j == 0) {
					bArr[i] = true;
					break;
				}
			}
		}

		int last = 0;
		int sum = 0;

		while (max >= min) {
			if (!bArr[max]) {
				sum += max;
				last = max;
			}

			max--;
		}

		if (last == 0) {
			bw.write(-1 + "");
		} else {
			bw.write(sum + "\n" + last);
		}

		bw.flush();
		bw.close();
	}

}
