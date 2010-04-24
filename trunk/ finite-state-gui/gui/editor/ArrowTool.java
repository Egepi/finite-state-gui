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

import gui.environment.AutomatonEnvironment;
import gui.viewer.AutomatonDrawer;
import gui.viewer.AutomatonPane;
import gui.viewer.CurvedArrow;

import java.awt.Component;
import java.awt.Point;
import java.awt.Rectangle;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.MouseEvent;
import java.awt.geom.Point2D;

import javax.swing.Icon;
import javax.swing.JMenuItem;
import javax.swing.JOptionPane;
import javax.swing.JPopupMenu;
import javax.swing.KeyStroke;

import automata.State;
import automata.Transition;
import debug.EDebug;

/**
 * The arrow tool is used mostly for editing existing objects.
 * 
 * @author Thomas Finley, Henry Qin
 */
@SuppressWarnings({"serial", "unchecked"})
public class ArrowTool extends Tool {
	/**
	 * Instantiates a new arrow tool.
	 * 
	 * @param view
	 *            the view where the automaton is drawn
	 * @param drawer
	 *            the object that draws the automaton
	 * @param creator
	 *            the transition creator used for editing transitions
	 */
	public ArrowTool(AutomatonPane view, AutomatonDrawer drawer,
			TransitionCreator creator) {
		super(view, drawer);
		//this.creator = creator;
	}

	/**
	 * Instantiates a new arrow tool.
	 * 
	 * @param view
	 *            the view where the automaton is drawn
	 * @param drawer
	 *            the object that draws the automaton
	 */
	public ArrowTool(AutomatonPane view, AutomatonDrawer drawer) 
	{
		super(view, drawer);
		//this.creator = TransitionCreator.creatorForAutomaton(getAutomaton(), getView());
	}

	public ArrowTool(EditCanvas view, AutomatonDrawer drawer, EditorPane editorPane) 
	{
		super(view, drawer);
		thePane = editorPane;
		//this.creator = TransitionCreator.creatorForAutomaton(getAutomaton(), getView());
	}

	/**
	 * Gets the tool tip for this tool.
	 * 
	 * @return the tool tip for this tool
	 */
	public String getToolTip() 
	{
		return "Arrow Tool";
	}

	/**
	 * Returns the tool icon.
	 * 
	 * @return the arrow tool icon
	 */
	protected Icon getIcon() 
	{
		java.net.URL url = getClass().getResource("/ICON/arrow.gif");
		return new javax.swing.ImageIcon(url);
	}

	/**
	 * On a mouse click, if this is a double click over a transition edit the
	 * transition. If this was a single click, then we select the transition.
	 * 
	 * @param event
	 *            the mouse event
	 */
	public void mouseClicked(MouseEvent event) 
	{
		if (event.getClickCount() == 1){
            Transition trans = getDrawer().transitionAtPoint(event.getPoint());
            if (trans != null){
                if (trans.isSelected){
                    trans.isSelected = false;
                    selectedTransition = null;
                } 
                else{
                    if (selectedTransition != null) selectedTransition.isSelected = false;
                    trans.isSelected = true;
                    selectedTransition = trans;
                     
                }
                return;
            }
        }
		Transition trans = getDrawer().transitionAtPoint(event.getPoint());
		if (trans == null){
			Rectangle bounds;
			bounds = new Rectangle(0, 0, -1, -1);
			getView().getDrawer().getAutomaton().selectStatesWithinBounds(bounds);
			getView().repaint();
			return;
		}
        //EDebug.print("Beginning to Edit with creator AHHHHH"+ creator.getClass());
		//creator.editTransition(trans, event.getPoint());

	}

	/**
	 * Possibly show a popup menu.
	 * 
	 * @param event
	 *            the mouse event
	 */
	protected void showPopup(MouseEvent event) 
	{
		// Should we show a popup menu?
		if (event.isPopupTrigger()) {
			Point p = getView().transformFromAutomatonToView(event.getPoint());
			if (lastClickedState != null && shouldShowStatePopup()) {
				stateMenu.show(lastClickedState, getView(), p);
			} 
			else if(lastClickedTransition != null)
			{
				transitionMenu.show(lastClickedTransition, getView(), p);
				
			}
			else 
			{
			}
		}
		
		//lastClickedState = null;
		//lastClickedTransition = null;
	}

	/**
	 * On a mouse press, allows the state to be dragged about unless this is a
	 * popup trigger.
	 */
	public void mousePressed(MouseEvent event) 
	{
		if (getDrawer().getAutomaton().getEnvironmentFrame() !=null)
    		((AutomatonEnvironment)getDrawer().getAutomaton().getEnvironmentFrame().getEnvironment()).saveStatus();
        else
            EDebug.print("I cannot preserve what you ask");
		initialPointClick.setLocation(event.getPoint());
		lastClickedState = getDrawer().stateAtPoint(event.getPoint());
		
		if (lastClickedState == null)
		{	
			lastClickedTransition = getDrawer().transitionAtPoint(event.getPoint());		
		}
		thePane.saveFields();
		if(lastClickedState != null)
		{
			thePane.updateLabels(lastClickedState);
			if(selectedTransition != null) selectedTransition.setSelected(false);
		}
		else if(lastClickedTransition != null)
		{
			thePane.updateLabels(lastClickedTransition);
		}
		else
		{
			thePane.hideAll();
			if(selectedTransition != null) selectedTransition.setSelected(false);
		}
		
		// Should we show a popup menu?
		if (event.isPopupTrigger())
		{
			showPopup(event);
		}

		if (lastClickedState != null) {
			initialPointState.setLocation(lastClickedState.getPoint());
			if(!lastClickedState.isSelected()){
				Rectangle bounds = new Rectangle(0, 0, -1, -1);
				getView().getDrawer().getAutomaton().selectStatesWithinBounds(bounds);
				getView().getDrawer().setSelectionBounds(bounds);
				lastClickedState.setSelect(true);
			}
			getView().repaint();
		}
		else if (lastClickedTransition != null) {
			initialPointClick.setLocation(event.getPoint());
		}	
		else {

			Rectangle bounds = new Rectangle(0, 0, -1, -1);
			getView().getDrawer().getAutomaton().selectStatesWithinBounds(bounds);
			getView().getDrawer().setSelectionBounds(bounds);
		}

        //reset the selectedTransition after an Undo has happened.

        
        Transition[] trans = getAutomaton().getTransitions();
        for (int i = 0; i < trans.length; i++)
            if (trans[i].isSelected){
                selectedTransition = trans[i];
                return;
            }
        

        selectedTransition = null;




	}

	/**
	 * Returns if the state popup menu should be shown whenever applicable.
	 * 
	 * @return <CODE>true</CODE> if the state menu should be popped up, <CODE>false</CODE>
	 *         if it should not be... returns <CODE>true</CODE> by default
	 */
	protected boolean shouldShowStatePopup() 
	{
		return true;
	}

	/**
	 * On a mouse drag, possibly move a state if the first press was on a state.
	 */
	public void mouseDragged(MouseEvent event) 
	{
		if (lastClickedState != null) {
			if (event.isPopupTrigger())
				return;
			Point p = event.getPoint();
			
			State[] states = getView().getDrawer().getAutomaton().getStates();
			for(int k = 0; k < states.length; k++){
				State curState = states[k];
				if(curState.isSelected()){
					int x = curState.getPoint().x + p.x - initialPointClick.x;
					int y = curState.getPoint().y + p.y - initialPointClick.y;
					curState.getPoint().setLocation(x, y);
					curState.setPoint(curState.getPoint());									
				}
			}
			initialPointClick = p;
			getView().repaint();
		} else if (lastClickedTransition != null) {
			if (event.isPopupTrigger())
				return;
			Point p = event.getPoint();
			State f = lastClickedTransition.getFromState(), t = lastClickedTransition
					.getToState();
			
			
			if (f != t) {
				Transition[] trans = getAutomaton().getTransitionsFromStateToState(f, t);
				for (int n = 0; n < trans.length; n++) {
					CurvedArrow arrow = (CurvedArrow) getView().getDrawer().transitionToArrowMap.get(trans[n]);

					
					getView().getDrawer().arrowToTransitionMap.put(arrow, trans[n]);
					getView().getDrawer().transitionToArrowMap.put(trans[n], arrow);
				}
			}
			initialPointClick.setLocation(p);
			getView().repaint();
			//EDebug.print(getView().getDrawer().selfTransitionMap);
		}
		else{
			Rectangle bounds;
			int nowX = event.getPoint().x;
			int nowY = event.getPoint().y;
			int leftX = initialPointClick.x;
			int topY = initialPointClick.y;
			if(nowX < initialPointClick.x) leftX = nowX;
			if(nowY < initialPointClick.y) topY = nowY;
			bounds = new Rectangle(leftX, topY, Math.abs(nowX-initialPointClick.x), Math.abs(nowY-initialPointClick.y));

            if (!transitionInFlux){
                getView().getDrawer().getAutomaton().selectStatesWithinBounds(bounds);
                getView().getDrawer().setSelectionBounds(bounds);
            }

			getView().repaint();
		}
        
        //Deal with transition dragging here
        if (selectedTransition != null){ //simply set ...but we need to get the initial point to be clever
            CurvedArrow ca = (CurvedArrow)getView().getDrawer().transitionToArrowMap.get(selectedTransition);

            Point myClickP = event.getPoint();
            Point2D control = ca.getCurve().getCtrlPt();

            if (transitionInFlux || Math.sqrt((control.getX() - myClickP.x)*(control.getX() - myClickP.x) 
                        + (control.getY() - myClickP.y)*(control.getY() - myClickP.y)) < 15){
                            selectedTransition.setControl(myClickP);
        //                System.out.println("Move it damn it");
                             ca.refreshCurve();
                             transitionInFlux = true;
                             return;
                        }

        }
	}

    private boolean transitionInFlux = false;

	/**
	 * On a mouse release, sets the tool to the "virgin" state.
	 */
	public void mouseReleased(MouseEvent event) 
	{
        transitionInFlux = false;
		if (event.isPopupTrigger())
		{
			showPopup(event);
		}
		
		State[] states = getView().getDrawer().getAutomaton().getStates();
		int count = 0;
		for(int k = 0; k < states.length; k++){			
			if(states[k].isSelected()){	
				count++;
			}
		}
		Rectangle bounds = getView().getDrawer().getSelectionBounds();
		if(count == 1 && bounds.isEmpty() && lastClickedState!=null) lastClickedState.setSelect(false);
		bounds = new Rectangle(0, 0, -1, -1);
		getView().getDrawer().setSelectionBounds(bounds);
		
		myLastClickedState = lastClickedState;
		myLastClickedTransition = lastClickedTransition;
		lastClickedState = null;
		lastClickedTransition = null;
		getView().repaint();
	}

	/**
	 * Returns the key stroke that will activate this tool.
	 * 
	 * @return the key stroke that will activate this tool
	 */
	public KeyStroke getKey() 
	{
		return KeyStroke.getKeyStroke('a');
	}

	/**
	 * Returns true if only changing the final stateness of a state should be
	 * allowed in the state menu.
	 */
	public boolean shouldAllowOnlyFinalStateChange() 
	{
		return false;
	}

	/**
	 * The contextual menu class for editing states.
	 */
    /*
     * I changed this from private class to protected class so I can 
     * remove the "Final State" option from Moore and Mealy machines.
     */
	protected class StateMenu extends JPopupMenu implements ActionListener 
	{
		public StateMenu() 
		{
			idleResponse = new JMenuItem("Idle Response");
			idleResponse.addActionListener(this);
			this.add(idleResponse);
						
			setName = new JMenuItem("Set Name");
			setName.addActionListener(this);
			this.add(setName);
			
			
}

		public void show(State state, Component comp, Point at) 
		{
			this.state = state;
//			if (state.getInternalName() != null) {
			show(comp, at.x, at.y);
		}

		public void actionPerformed(ActionEvent e) 
		{
			JMenuItem item = (JMenuItem) e.getSource();
            if (getDrawer().getAutomaton().getEnvironmentFrame() !=null)
                ((AutomatonEnvironment)getDrawer().getAutomaton().getEnvironmentFrame().getEnvironment()).saveStatus();
            
            /***********************************************************/
            /*Added for project Lifelike */
			if (item == idleResponse)
			{
				String oldIdleLabel = state.getIdleResponses();
				String idleLabel = (String) JOptionPane.showInputDialog(this,
						"Input idle responses", "Idle Responses",
				JOptionPane.QUESTION_MESSAGE, null, null, oldIdleLabel);
				if (idleLabel == null)
					return;
				if (idleLabel.equals(""))
					idleLabel = null;	
				state.setIdleResponses(idleLabel);
				thePane.updateLabels(state);
			}
			/************************************************************/
            
			getView().repaint();
		}
		
	    private State state;
		
		protected JMenuItem setName, idleResponse;
	}

	/**
	 * The contextual menu class for editing transitions.
	 */
	private class TransitionMenu extends JPopupMenu implements ActionListener
	{
		public TransitionMenu()
		{
			keywords = new JMenuItem("Keywords");
			keywords.addActionListener(this);
			this.add(keywords);
			response = new JMenuItem("Response");
			response.addActionListener(this);
			this.add(response);
		}
		public void show(Transition lastClickedTransition, Component comp, Point at) 
		{
			this.transition = lastClickedTransition;
			show(comp, at.x, at.y);
		}
		public void actionPerformed(ActionEvent e) 
		{
			JMenuItem item = (JMenuItem) e.getSource();
			/************************************************************/
			/*Added for project Lifelike */
			if (item == response)
			{
				String oldResponse = transition.getResponses();
				String newResponse = (String) JOptionPane.showInputDialog(this,
						"Input Responses", "Responses",
				JOptionPane.QUESTION_MESSAGE, null, null, oldResponse);
				if (newResponse == null)
					return;
				if (newResponse.equals(""))
					response = null;	
				transition.setResponses(newResponse);
				thePane.updateLabels(transition);
			}
			/************************************************************/
			/************************************************************/
			/*Added for project Lifelike */
			if (item == keywords)
			{
				String oldKeywords = transition.getKeywords();
				String newKeywords = (String) JOptionPane.showInputDialog(this,
						"Input keywords", "Keywords",
				JOptionPane.QUESTION_MESSAGE, null, null, oldKeywords);
				if (newKeywords == null)
					return;
				if (newKeywords.equals(""))
					newKeywords = null;	
				transition.setKeywords(newKeywords);
				thePane.updateLabels(transition);
			}
			/************************************************************/
		}
		private Transition transition;
		private JMenuItem response, keywords;
	}

	/**
	 * The contextual menu class for context clicks in blank space.
	 */
		
	
	public State getLastState()
	{
		return this.myLastClickedState;
	}
	public Transition getLastTransition()
	{
		return this.myLastClickedTransition;
	}
	
	private EditorPane thePane;
	/** The state that was last clicked. */
	private State lastClickedState = null;

	/** The transition that was last clicked. */
	private Transition lastClickedTransition = null;
	
	/** The initial point of the state. */
	private Point initialPointState = new Point();

	/** The initial point of the click. */
	private Point initialPointClick = new Point();

	/** The state menu. */
    /*
     * I changed it to protected because I needed to mess with
     * it in a subclass. This is to remove the "Final State"
     * option in Moore and Mealy machines.
     */
	protected StateMenu stateMenu = new StateMenu();

	/** The transition menu. */
	private TransitionMenu transitionMenu = new TransitionMenu();

	private Transition selectedTransition = null;
    
    private State myLastClickedState = null;
    private Transition myLastClickedTransition = null;
}