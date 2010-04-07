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





package gui.action;

import gui.environment.*;
import gui.menu.MenuBarCreator;

import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.KeyEvent;
import java.awt.event.WindowAdapter;
import java.awt.event.WindowEvent;
import java.io.Serializable;
import javax.swing.*;


/**
 * The <CODE>NewAction</CODE> handles when the user decides to create some new
 * environment, that is, some sort of new automaton, or grammar, or regular
 * expression, or some other such editable object.
 * 
 * @author Thomas Finley
 */
@SuppressWarnings({"serial"})
public class NewAction extends RestrictedAction {
	/**
	 * Instantiates a new <CODE>NewAction</CODE>.
	 */
	public NewAction() {
		super("New...", null);
		putValue(ACCELERATOR_KEY, KeyStroke.getKeyStroke(KeyEvent.VK_N,
				MAIN_MENU_MASK));
	}

	/**
	 * Shows the new machine dialog box.
	 * 
	 * @param event
	 *            the action event
	 */
	public void actionPerformed(ActionEvent event) {
		showNew();
	}
	
	/**
	 * Dispose of environment dialog
	 * by Moti Ben-Ari
	 */
    public static void closeNew() {
        DIALOG.dispose();
        DIALOG = null;
    }

	/**
	 * Shows the new environment dialog.
	 */
	public static void showNew() {

		if (DIALOG == null)
			DIALOG = new NewDialog();
		//DIALOG.setVisible(true);
		//DIALOG.toFront();
		if (secondWindow)
		{
			secondWindow = false;
			gui.Main.setDontQuit(false);
			createWindow(new automata.fsa.FiniteStateAutomaton());
			
		}
		else
		{
			System.exit(0);
		}
		
	}

	/**
	 * Hides the new environment dialog.
	 */
	public static void hideNew() {
		DIALOG.setVisible(false);
	}

	/**
	 * Called once a type of editable object is choosen. The editable object is
	 * passed in, the dialog is hidden, and the window is created.
	 * 
	 * @param object
	 *            the object that we are to edit
	 */
	private static void createWindow(Serializable object) {
		DIALOG.setVisible(false);
		FrameFactory.createFrame(object);
	}

	/** The dialog box that allows one to create new environments. */
	private static class NewDialog extends JFrame {
		/**
		 * Instantiates a <CODE>NewDialog</CODE> instance.
		 */
		public NewDialog() {
			// super((java.awt.Frame)null, "New Document");
			super("JFLAP 7.0");
			getContentPane().setLayout(new GridLayout(0, 1));
			initMenu();
			initComponents();
			setResizable(false);
			this.pack();
			this.setLocation(50, 50);

			this.addWindowListener(new WindowAdapter() {
				public void windowClosing(WindowEvent event) {
					if (Universe.numberOfFrames() > 0) {
						NewDialog.this.setVisible(false);
					} else {
						QuitAction.beginQuit();
					}
				}
			});
		}

		private void initMenu() {
			// Mini menu!
			JMenuBar menuBar = new JMenuBar();
			JMenu menu = new JMenu("File");
			if (Universe.CHOOSER != null) {
				MenuBarCreator.addItem(menu, new OpenAction());
			}
			try {
				SecurityManager sm = System.getSecurityManager();
				if (sm != null)
					sm.checkExit(0);
				MenuBarCreator.addItem(menu, new QuitAction());
			} catch (SecurityException e) {
				// Well, can't exit anyway.
			}

            menuBar.add(menu);
			//menu = new JMenu("Help");
			//MenuBarCreator.addItem(menu, new NewHelpAction());
			//MenuBarCreator.addItem(menu, new AboutAction());
			//menuBar.add(menu);
            menu = new JMenu("Batch");
            //MenuBarCreator.addItem(menu, new TestAction());
            //menuBar.add(menu);
            menu = new JMenu("Preferences");

            JMenu tmPrefMenu = new JMenu("Turing Machine Preferences");
            tmPrefMenu.add(Universe.curProfile.getTuringFinalCheckBox());
            tmPrefMenu.add(Universe.curProfile.getAcceptByFinalStateCheckBox());
            tmPrefMenu.add(Universe.curProfile.getAcceptByHaltingCheckBox());
            tmPrefMenu.add(Universe.curProfile.getAllowStayCheckBox());

            MenuBarCreator.addItem(menu, new EmptyStringCharacterAction());
//            menu.add(Universe.curProfile.getTuringFinalCheckBox());
            menu.add(new SetUndoAmountAction());

            menu.add(tmPrefMenu);

            menuBar.add(menu);
			setJMenuBar(menuBar);
		}

		private void initComponents() {
			JButton button = null;
			// Let's hear it for sloth!

			button = new JButton("Finite Automaton");
			button.addActionListener(new ActionListener() {
				public void actionPerformed(ActionEvent e) {
					createWindow(new automata.fsa.FiniteStateAutomaton());
				}
			});
			getContentPane().add(button);
 
		}
	}

	/** The universal dialog. */
	private static NewDialog DIALOG = null;
	private static boolean secondWindow = true;
}
