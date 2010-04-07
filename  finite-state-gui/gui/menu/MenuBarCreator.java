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





package gui.menu;


import javax.swing.*;
import gui.environment.Environment;
import gui.environment.AutomatonEnvironment;
import gui.environment.EnvironmentFrame;
import gui.environment.Universe;
import gui.action.*;

/**
 * The <CODE>MenuBarCreator</CODE> is a creator of the menu bars for the FLAP
 * application.
 * 
 * @author Thomas Finley
 */

public class MenuBarCreator {
	/**
	 * Instantiates the menu bar.
	 * 
	 * @param frame
	 *            the environment frame that holds the environment and object
	 * @return the menu bar appropriate for the environment
	 */
	public static JMenuBar getMenuBar(EnvironmentFrame frame) {
		JMenuBar bar = new JMenuBar();
		JMenu menu;

		menu = getFileMenu(frame);
		if (menu.getItemCount() > 0)
			bar.add(menu);

        CloseButton dismiss = new CloseButton(frame.getEnvironment());
        bar.add(Box.createGlue());
        bar.add(dismiss);
        
		return bar;
	}

	/**
	 * Adds an action to a menu with the accelerator key set.
	 * 
	 * @param menu
	 *            the menu to add the action to
	 * @param a
	 *            the action to create the menu item for
	 */
	public static void addItem(JMenu menu, Action a) {
		JMenuItem item = new JMenuItem(a);
		item.setAccelerator((KeyStroke) a.getValue(Action.ACCELERATOR_KEY));
		menu.add(item);
	}

	/**
	 * Instantiates the file menu.
	 * 
	 * @param frame
	 *            the environment frame that holds the environment and object
	 * @return a file menu
	 */
	private static JMenu getFileMenu(EnvironmentFrame frame) {
		Environment environment = frame.getEnvironment();
		JMenu menu = new JMenu("File");
		addItem(menu, new NewAction());
		SecurityManager sm = System.getSecurityManager();
		if (Universe.CHOOSER != null) {
			// Can't open and save files.
			addItem(menu, new OpenAction());
			addItem(menu, new SaveAction(environment));
			addItem(menu, new SaveAsAction(environment));
			JMenu saveImageMenu;
			saveImageMenu = new JMenu("Save Image As...");
			saveImageMenu.add(new SaveGraphJPGAction(environment, menu));
			saveImageMenu.add(new SaveGraphPNGAction(environment, menu));
			saveImageMenu.add(new SaveGraphGIFAction(environment, menu));
			saveImageMenu.add(new SaveGraphBMPAction(environment, menu));
            if (environment instanceof AutomatonEnvironment) //this is strictly for non-Grammar
                saveImageMenu.add(new ExportAction(environment));
			menu.add(saveImageMenu);
            
		}
		else{
			addItem(menu, new OpenURLAction());
		}
		addItem(menu, new CloseAction(environment));
		addItem(menu, new CloseWindowAction(frame));
		/*
		try {
			if (sm != null)
				sm.checkPrintJobAccess();
			addItem(menu, new PrintAction(environment));
		} catch (SecurityException e) {
			// Damn. Can't print!
		}
		*/
		try {
			if (sm != null)
				sm.checkExit(0);
			addItem(menu, new QuitAction());
		} catch (SecurityException e) {
			// Well, can't exit anyway.
		}

//        if (environment instanceof AutomatonEnvironment){
//            addItem(menu, new SetUndoAmountAction());
//        }


		return menu;
	}
}
