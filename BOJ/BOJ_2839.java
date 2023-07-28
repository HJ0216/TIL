import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;

public class Main {

	public static void main(String[] args) throws IOException {
		BufferedWriter bw = new BufferedWriter(new OutputStreamWriter(System.out));
		BufferedReader br = new BufferedReader(new InputStreamReader(System.in));

		int kg = Integer.parseInt(br.readLine());

		int i = 1;
		int j = 1;

		boolean b = false;

		Loop: for (i = 0; i <= kg / 3; i++) {
			for (j = 0; j <= kg / 5; j++) {
				if (3 * i + 5 * j == kg) {
					b = true;
					break Loop;
				}
			}
		}

		if (b) {
			bw.write((i + j) + "");
		} else {
			bw.write("-1");
		}

		bw.flush();
		bw.close();

	}

}
