package boj;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;

public class Main {
	public static void main(String[] args) throws Exception {
		BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
		BufferedWriter bw = new BufferedWriter(new OutputStreamWriter(System.out));

		String s = br.readLine();
		
		int count = 0;

		if(!s.equals(" ")){
			s = s.trim();			
			s = s.replace(" ", "_");

			for(int i=0; i<s.length(); i++) {
				if((s.charAt(i))==('_')) {
					count++;
				}			
			}
			bw.write((count+1) + "");
			
		} else {bw.write(count + "");}
		bw.flush();
		bw.close();
	}
}
