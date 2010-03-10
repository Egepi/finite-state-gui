/*
 *  JFLAP - Formal Languages and Automata Package
 * 
 * 
 *  Susan H. Rodger
 *  Computer Science Department
 *  Duke University
 *  August 27, 2009

 *  Copyright (c) 2002-2009
 *  All rights reserved.

 *  JFLAP is open source software. Please see the LICENSE for terms.
 *
 */


/**
 * This is the class that starts JFLAP.
 * 
 * @author Thomas Finley
 * @author Moti Ben-Ari
 *   All code moved to gui.Main
 *   Parameter dontQuit false for command line invocation
 */

public class JFLAP {
	public static void main(String[] args) {
		gui.Main.main(args, false);
	}
}
