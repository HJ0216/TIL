import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;

public class Main {

	static StringBuffer sb = new StringBuffer();

	public static void main(String[] args) throws IOException {
		BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
		BufferedWriter bw = new BufferedWriter(new OutputStreamWriter(System.out));

		String s;
		while ((s = br.readLine()) != null) {
			check(s);
		}

		bw.append(sb + "");

		bw.flush();
		bw.close();
	}

	public static void check(String s) {
		int small_letter = 0;
		int capital_letter = 0;
		int number_letter = 0;
		int blank_letter = 0;

		int len = s.length();

		for (int i = 0; i < len; i++) {
			char c = s.charAt(i);

			if (c > 96) {
				small_letter++;
			} else if (c > 64) {
				capital_letter++;
			} else if (c > 47) {
				number_letter++;
			}
		}

		blank_letter = len - (small_letter + capital_letter + number_letter);

		sb.append(small_letter + " " + capital_letter + " " + number_letter + " " + blank_letter + "\n");

	}

}
