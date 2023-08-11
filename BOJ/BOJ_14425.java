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

		StringTokenizer st = new StringTokenizer(br.readLine());
		int num1 = Integer.parseInt(st.nextToken());
		int num2 = Integer.parseInt(st.nextToken());

		String[] sArr1 = new String[num1];
		for (int i = 0; i < num1; i++) {
			sArr1[i] = br.readLine();
		}

		int cnt = 0;
		for (int i = 0; i < num2; i++) {
			cnt += check(sArr1, br.readLine());
		}

		bw.write(cnt + "");
		bw.flush();
		bw.close();
	}

	public static int check(String[] sArr1, String s) {
		int cnt = 0;

		for (int i = 0; i < sArr1.length; i++) {
			if (sArr1[i].equals(s)) {
				cnt++;
			}
		}

		return cnt;

	}

}
