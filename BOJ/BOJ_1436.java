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

		int i = 0;
		int cnt = 0;
		for (i = 666; cnt != N; i++) {
			if (String.valueOf(i).contains("666")) {
				cnt++;
			}
		}

		bw.write((i - 1) + "");

		bw.flush();
		bw.close();

	}

}
