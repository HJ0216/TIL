import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;

public class Main {

	public static void main(String[] args) throws IOException {
		BufferedWriter bw = new BufferedWriter(new OutputStreamWriter(System.out));
		BufferedReader br = new BufferedReader(new InputStreamReader(System.in));

		int N = Integer.parseInt(br.readLine());

		int cnt = 0;

		int i = 1;
		int j = 1;
		Loop: for (i = 1;; i++) {
			for (j = 1; j <= i; j++) {
				cnt++;
				if (cnt == N) {
					break Loop;
				}
			}
		}

		if (i % 2 == 0) {
			bw.write(j + "/" + (i + 1 - j));
		} else {
			bw.write((i + 1 - j) + "/" + j);
		}

		bw.flush();
		bw.close();

	}

}
