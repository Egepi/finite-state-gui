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





package gui.editor;

import gui.viewer.AutomatonDrawer;
import gui.viewer.SelectionDrawer;

import java.awt.BorderLayout;
import java.awt.Color;
import java.awt.Dimension;
import java.awt.Graphics;

import javax.swing.BorderFactory;
import javax.swing.JComponent;
import javax.swing.JLabel;

import javax.swing.JPanel;
import javax.swing.JScrollPane;
import javax.swing.JTextPane;
import javax.swing.border.BevelBorder;

import automata.Automaton;
import automata.State;
import automata.Transition;
/**
 * This is a view that holds a tool bar and the canvas where the automaton is
 * displayed.
 * 
 * @author Thomas Finley
 */
@SuppressWarnings({"serial"})
public class EditorPane extends JComponent{
	/**
	 * Instantiates a new editor pane for the given automaton.
	 * 
	 * @param automaton
	 *            the automaton to create the editor pane for
	 */
	public EditorPane(Automaton automaton) 
	{
		this(new SelectionDrawer(automaton));
	}

	/**
	 * Instantiates a new editor pane with a tool box.
	 */
	public EditorPane(Automaton automaton, ToolBox box) 
	{
		this(new SelectionDrawer(automaton), box);
	}

	/**
	 * Instantiates a new editor pane with a given automaton drawer.
	 * 
	 * @param drawer
	 *            the special automaton drawer for this editor
	 */
	public EditorPane(AutomatonDrawer drawer) 
	{
		this(drawer, new DefaultToolBox());
	}

	/**
	 * Instantiates a new editor pane with a given automaton drawer.
	 * 
	 * @param drawer
	 *            the special automaton drawer for this editor
	 * @param box
	 *            the tool box to get the tools from
	 */
	public EditorPane(AutomatonDrawer drawer, ToolBox box) 
	{
		this(drawer, box, false);
	}

	/**
	 * Instantiates a new editor pane with a given automaton drawer.
	 * 
	 * @param drawer
	 *            the special automaton drawer for this editor
	 * @param box
	 *            the tool box to get teh tools from
	 * @param fit
	 *            <CODE>true</CODE> if the editor should resize its view to
	 *            fit the automaton; note that this can be <I>very</I> annoying
	 *            if the automaton changes
	 */
	public EditorPane(AutomatonDrawer drawer, ToolBox box, boolean fit)
	{
		pane = new EditCanvas(drawer, fit);
		pane.setCreator(this);
		this.drawer = drawer;
		this.automaton = drawer.getAutomaton();
		this.setLayout(new BorderLayout());
		
		JPanel superpane = new JPanel();
		superpane.setLayout(new BorderLayout());
		superpane.add(new JScrollPane(pane,
				JScrollPane.VERTICAL_SCROLLBAR_ALWAYS,
				JScrollPane.HORIZONTAL_SCROLLBAR_ALWAYS), BorderLayout.CENTER);
		superpane.setBorder(new BevelBorder(BevelBorder.LOWERED));

		toolbar = new gui.editor.ToolBar(pane, drawer, box , this);
		pane.setToolBar(toolbar);

		/* Where side pane is added */
		
		stateName = new JTextPane();
		stateName.setPreferredSize(new Dimension(190, 20));
		
		keywords = new JTextPane();
		keywords.setPreferredSize(new Dimension(190,100));
		
		response = new JTextPane();
		response.setPreferredSize(new Dimension(190,100));		

		idleResponse = new JTextPane();
		idleResponse.setPreferredSize(new Dimension(190,100));
		
		
		stateName.setBorder(BorderFactory.createLineBorder(Color.black));
		idleResponse.setBorder(BorderFactory.createLineBorder(Color.black));
		response.setBorder(BorderFactory.createLineBorder(Color.black));
		keywords.setBorder(BorderFactory.createLineBorder(Color.black));
		
		
		keywordsLabel = new JLabel();
		keywordsLabel.setText("Keywords");
				
		responseLabel = new JLabel();
		responseLabel.setText("Responses");
		
		idleResponseLabel = new JLabel();
		idleResponseLabel.setText("Idle Responses");
				
		nameLabel = new JLabel();
		nameLabel.setText("Name");
		
		editPanel = new JPanel();
		editPanel.setPreferredSize(new Dimension(200, 500));
		editPanel.add(nameLabel);
		editPanel.add(stateName);
		editPanel.add(keywordsLabel);
		editPanel.add(keywords);
		editPanel.add(responseLabel);
		editPanel.add(response);
		editPanel.add(idleResponseLabel);
		editPanel.add(idleResponse);
		
		editPanel.setVisible(false);
		this.hideAll();
		
		
		this.add(superpane, BorderLayout.CENTER);
		this.add(toolbar, BorderLayout.NORTH);
		//this.add(new AutomatonSizeSlider(pane, drawer), BorderLayout.SOUTH);
		this.add(editPanel, BorderLayout.EAST);

	}
	
	

	/**
	 * Returns the toolbar for this editor pane.
	 * 
	 * @return the toolbar of this editor pane
	 */
	public gui.editor.ToolBar getToolBar() {
		return toolbar;
	}

	/**
	 * Returns the automaton drawer for the editor pane canvas.
	 * 
	 * @return the drawer that draws the automaton being edited
	 */
	public AutomatonDrawer getDrawer() {
		return pane.getDrawer();
	}

	/**
	 * Returns the automaton pane.
	 * 
	 * @return the automaton pane
	 */
	public EditCanvas getAutomatonPane() {
		return pane;
	}

	/**
	 * Prints this component. This will print only the automaton section of the
	 * component.
	 * 
	 * @param g
	 *            the graphics object to paint to
	 */
	public void printComponent(Graphics g) {
		pane.print(g);
	}

	/**
	 * Children are not painted here.
	 * 
	 * @param g
	 *            the graphics object to paint to
	 */
	public void printChildren(Graphics g) {

	}

	/**
	 * Returns the automaton pane.
	 * 
	 * @return the automaton pane
	 */
	public Automaton getAutomaton() {
		return automaton;
	}


	JPanel editPanel;
	
	JTextPane keywords;
	JTextPane response;
	JTextPane idleResponse;
	JTextPane stateName;
	
	JLabel idleResponseLabel;
	JLabel responseLabel;
	JLabel keywordsLabel;
	JLabel nameLabel;
	
	/** The automaton. */
	protected Automaton automaton;

	/** The automaton drawer. */
	protected AutomatonDrawer drawer;

	/** The automaton pane. */
	protected EditCanvas pane;

	/** The tool bar. */
	protected gui.editor.ToolBar toolbar;


	void saveFields() {
		Tool myTool = toolbar.getCurrentTool();
		if(myTool.getToolTip().equalsIgnoreCase("Arrow Tool"))
		{
			ArrowTool myArrowTool = (ArrowTool) myTool;
			State tempState = myArrowTool.getLastState();
			Transition tempTransition = myArrowTool.getLastTransition();
			if(tempState != null)
			{
				tempState.setIdleResponses(this.idleResponse.getText());
				tempState.setName(this.stateName.getText());
			}
			else if(tempTransition != null)
			{
				tempTransition.setKeywords(this.keywords.getText());
				tempTransition.setResponses(this.response.getText());
			}
			else
			{
				
			}
		}
		//System.out.println("" + myTool);

	}
	
	public void updateLabels(State lastClickedState) {
		this.editPanel.setVisible(true);
		//Hide unneeded stuff
		this.response.setText("");
		this.response.setVisible(false);
		this.responseLabel.setVisible(false);
		this.keywords.setText("");
		this.keywords.setVisible(false);
		this.keywordsLabel.setVisible(false);
		
		//Get the state properties
		this.nameLabel.setVisible(true);
		this.stateName.setVisible(true);
		this.stateName.setText(lastClickedState.getName());
		
		this.idleResponse.setVisible(true);
		this.idleResponseLabel.setVisible(true);
		this.idleResponse.setText(lastClickedState.getIdleResponses());
		this.idleResponse.requestFocus();
	}

	public void updateLabels(Transition lastClickedTransition) 
	{
		this.editPanel.setVisible(true);
		this.idleResponse.setVisible(false);
		this.idleResponseLabel.setVisible(false);
		this.idleResponse.setText("");
		this.nameLabel.setVisible(false);
		this.stateName.setVisible(false);
		this.stateName.setText("");

		//Get Transition properties
		this.response.setText(lastClickedTransition.getResponses());
		this.response.setVisible(true);
		this.responseLabel.setVisible(true);
		this.keywords.setText(lastClickedTransition.getKeywords());
		this.keywords.setVisible(true);
		this.keywordsLabel.setVisible(true);
		this.keywords.requestFocus();

	}

	public void hideAll() 
	{
		this.editPanel.setVisible(false);
		//Hide unneeded stuff
		this.response.setText("");
		this.response.setVisible(false);
		this.responseLabel.setVisible(false);
		this.keywords.setText("");
		this.keywords.setVisible(false);
		this.keywordsLabel.setVisible(false);
		this.idleResponse.setVisible(false);
		this.idleResponseLabel.setVisible(false);
		this.idleResponse.setText("");
		this.nameLabel.setVisible(false);
		this.stateName.setVisible(false);
		this.stateName.setText("");
	}

}
