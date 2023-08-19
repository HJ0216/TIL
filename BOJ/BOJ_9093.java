import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.util.Stack;
import java.util.StringTokenizer;

public class Main {

	static StringBuffer sb = new StringBuffer();

	public static void main(String[] args) throws IOException {
		BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
		BufferedWriter bw = new BufferedWriter(new OutputStreamWriter(System.out));

		int N = Integer.parseInt(br.readLine());

		for (int i = 0; i < N; i++) {
			StringTokenizer st = new StringTokenizer(br.readLine());

			while (st.hasMoreTokens()) {
				make_stack(st.nextToken());
			}

			sb.append("\n");
		}

		bw.write(sb + "");

		bw.flush();
		bw.close();
	}

	public static void make_stack(String s) {
		Stack<Character> stack = new Stack<>();
		for (int j = 0; j < s.length(); j++) {
			stack.push(s.charAt(j));
		}

		for (int j = 0; j < s.length(); j++) {
			sb.append(stack.pop() + "");
		}

		sb.append(" ");

	}

}
