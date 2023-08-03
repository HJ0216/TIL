import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.util.StringTokenizer;

public class Main {

	public static void main(String[] args) throws IOException {
		BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
		BufferedWriter bw = new BufferedWriter(new OutputStreamWriter(System.out));

		StringTokenizer st = new StringTokenizer(br.readLine(), " ");

		int A = Integer.parseInt(st.nextToken());
		int B = Integer.parseInt(st.nextToken());

		int C = Integer.parseInt(br.readLine());
		int N = Integer.parseInt(br.readLine());
		
		int x = 1;
		for (x = 1; x <= N; x++) {
			if ((C - A) * x >= B) {
				break;
			}
		}

		if (x <= N && A<=C) {
			bw.write("1");
		} else {
			bw.write("0");
		}

		bw.flush();
		bw.close();
	}

}
