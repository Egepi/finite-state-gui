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





package gui.environment;

import file.Encoder;
import java.awt.*;
import java.io.File;
import java.io.Serializable;
import java.util.*;

import javax.swing.*;
import javax.swing.event.ChangeEvent;
import javax.swing.event.ChangeListener;

//import sun.security.util.Debug;

/**
 * The environment class is the central view that manages various "hangers on"
 * of an object. By "hanger on" I mean a component that has some relevance to
 * the object that this environment contains. For example, each <CODE>Environment</CODE>
 * instance has, at minimum some sort of component whereby this structure can be
 * edited. The <CODE>Environment</CODE> instance keeps track of and displays
 * these various components.
 * 
 * @see gui.environment.EnvironmentFrame
 * @see gui.environment.tag
 * 
 * @author Thomas Finley
 */
@SuppressWarnings({"serial", "unchecked"})
public abstract class Environment extends JPanel {


    /**
	 * Instantiates a new environment for the given object. This environment is
	 * assumed to have no native file to which to save the object. One should
	 * use the <CODE>setFile</CODE> object if this environment should have
	 * one.
	 * 
	 * @param object
	 *            assumed to be some sort of object that this environment holds;
	 *            subclasses may provide more stringent requirements for this
	 *            kind of object
	 */
	public Environment(Serializable object) {
		theMainObject = object;
		clearDirty();
		initView();
	}

	/**
	 * Returns the main object for this environment. This is the object that was
	 * passed in for the constructor.
	 * 
	 * @return the main object for this environment
	 */
	public Serializable getObject() {
		return theMainObject;
	}

	/**
	 * Adds a file change listener to this environment.
	 * 
	 * @param listener
	 *            the listener to add
	 */
	public void addFileChangeListener(FileChangeListener listener) {
		fileListeners.add(listener);
	}

	/**
	 * Removes a file change listener from this environment.
	 * 
	 * @param listener
	 *            the listener to remove
	 */
	public void removeFileChangeListener(FileChangeListener listener) {
		fileListeners.remove(listener);
	}

	/**
	 * Distributes the given file change event among all file change listeners.
	 * 
	 * @param event
	 *            the file change event to distribute
	 */
	protected void distributeFileChangeEvent(FileChangeEvent event) {
		Iterator it = fileListeners.iterator();
		while (it.hasNext()) {
			FileChangeListener listener = (FileChangeListener) it.next();
			listener.fileChanged(event);
		}
	}

	/**
	 * Returns the file that this <CODE>Environment</CODE> has loaded itself
	 * from.
	 * 
	 * @return the file object that is owned by this environment as the place to
	 *         store the serializable object, or <CODE>null</CODE> if this
	 *         environment currently has no file
	 */
	public File getFile() {
		return file;
	}

	/**
	 * Sets the file owned by this <CODE>Environment</CODE> as the default
	 * location to save the object.
	 * 
	 * @param file
	 *            the new file for the environment
	 */
	public void setFile(File file) {
		File oldFile = this.file;
		this.file = file;
		distributeFileChangeEvent(new FileChangeEvent(this, oldFile));
	}


    public void setMultipleObjects(ArrayList objects) {     
        this.myObjects = objects;
    }

	/**
	 * Sets the encoder to use when writing this environment's file. This should
	 * be set when the file is ever written, or when a file is read and the
	 * format it was read in has a corresponding encoder.
	 * 
	 * @param encoder
	 *            the encoder for this
	 */
	public void setEncoder(Encoder encoder) {
		this.encoder = encoder;
	}

	/**
	 * Gets the encoder to be used when saving this file.
	 * 
	 * @return the encoder to use to save this file, or <CODE>null</CODE> if
	 *         no encoder has been chosen yet
	 */
	public Encoder getEncoder() {
		return encoder;
	}

	/**
	 * A helper function to set up the GUI components.
	 */
	private void initView() {
		this.setLayout(new BorderLayout());
		tabbed = new JTabbedPane();
		super.add(tabbed, BorderLayout.CENTER);
		// So that when the user changes the view by clicking in the
		// tabbed pane, this knows about it.
		tabbed.addChangeListener(new ChangeListener() {
			public void stateChanged(ChangeEvent event) {
				distributeChangeEvent();
			}
		});
	}

	/**
	 * Returns if a particular component is part of this environment, as through
	 * addition through one of the <CODE>add</CODE> methods
	 * 
	 * @param component
	 *            the component to check for membership in this environment
	 * @see #add
	 * @see #remove
	 */
	public boolean contains(Component component) {
		return tabbed.indexOfComponent(component) != -1;
	}

	/**
	 * Adds a component with the specified name. This is the same as the other
	 * add method, except without that tag field, which is assumed to be a tag
	 * object with no other tagness ascribed to it (i.e. a generic tag). That
	 * is, the component is assumed to have an empty tag.
	 * 
	 * @param component
	 *            the component to add, which should be unique for this
	 *            environment
	 * @param name
	 *            the name this component should be labeled with, which is not
	 *            necessarily a unique label
	 * @see #add(Component, String, Tag)
	 */
	//public void add(Component component, String name) {
	//	this.add(component, name);
	//}

	/**
	 * Programmatically sets the currently active component in this environment.
	 * 
	 * @param component
	 *            the component to make active
	 * @see #getActive
	 */
	public void setActive(Component component) {
		tabbed.setSelectedComponent(component);
		// The change event should be automatically distributed by the
		// model of the tabbed pane
	}

	/**
	 * Returns the currently active component in this environment.
	 * 
	 * @return the currently active component in this environment
	 * @see #setActive
	 */
	public Component getActive() {
		return tabbed.getSelectedComponent();
	}

	/**
	 * Returns whether or not the component is enabled, that is, selectable.
	 * 
	 * @param component
	 *            the component to check for enabledness
	 * @return <CODE>true</CODE> if the given component is enabled, <CODE>false</CODE>
	 *         if the given component is disabled
	 */
	public boolean isEnabled(Component component) {
		return tabbed.isEnabledAt(tabbed.indexOfComponent(component));
	}

	/**
	 * Sets whether or not a component is enabled.
	 * 
	 * @param component
	 *            the component to change the enabledness
	 * @param enabled
	 *            <CODE>true</CODE> if the component should be made enabled,
	 *            <CODE>false</CODE> if it should be made disabled
	 */
	public void setEnabled(Component component, boolean enabled) {
		tabbed.setEnabledAt(tabbed.indexOfComponent(component), enabled);
		distributeChangeEvent();
	}

	/**
	 * Adds a change listener to this object. The listener will receive events
	 * whenever the active component changes, or when components are made
	 * enabled or disabled, or when components are added or removed.
	 * 
	 * @param listener
	 *            the listener to add
	 */
	public void addChangeListener(ChangeListener listener) {
		changeListeners.add(listener);
	}

	/**
	 * Removes a change listener from this object.
	 * 
	 * @param listener
	 *            the listener to remove
	 */
	public void removeChangeListener(ChangeListener listener) {
		changeListeners.remove(listener);
	}

	/**
	 * Distributes a change event to all listeners.
	 */
	protected void distributeChangeEvent() {
		
		ChangeEvent e = new ChangeEvent(this);
		Iterator it = (new HashSet(changeListeners)).iterator();
		while (it.hasNext())
			((ChangeListener) it.next()).stateChanged(e);
	}

	/**
	 * Removes a component from this environment.
	 * 
	 * @param component
	 *            the component to remove
	 */
	public void remove(Component component) {
		tabbed.remove(component);
		distributeChangeEvent();
	}

	/**
	 * Returns an array containing all components.
	 * 
	 * @return an array containing all components.
	 */
	public Component[] getComponents() {
		Component[] comps = new Component[tabbed.getTabCount()];
		for (int i = 0; i < comps.length; i++)
			comps[i] = tabbed.getComponentAt(i);
		return comps;
	}
	
	/**
	 * Returns if this environment dirty. An environment is called dirty if the
	 * object it holds has been modified since the last save.
	 * 
	 * @return <CODE>true</CODE> if the environment is dirty, <CODE>false</CODE>
	 *         otherwise
	 */
	public boolean isDirty() {
		return dirty;
	}

	/**
	 * Sets the dirty bit. This should be called if the object is changed.
	 */
	public void setDirty() {
//		EDebug.print("Change has come");
		dirty = true;
	}

	/**
	 * Clears the dirty bit. This should be called when the object is saved to a
	 * file, or is in some other such state that a save is not required.
	 */
	public void clearDirty() {
		dirty = false;
	}
	
	public void setNewMainObject(Serializable obj){
		theMainObject = obj;
	
	}
	
	public void resizeSplit(){
		//super.setSize(width, height);
		if(myObjects != null && this.tabbed != null){
			if(myObjects.size() > 0 && this.tabbed.getTabCount() == 1){
			}
		}
		
	}
	
	
    /**For Testing multiple objects*/
    public ArrayList myObjects;
    public ArrayList myTestStrings;
    public ArrayList myTransducerStrings;
	/** The encoder for this document. */
	private Encoder encoder = null;

	/** The tabbed pane for this environment. */
	public JTabbedPane tabbed;

	/** The collection of change listeners for this object. */
	private transient HashSet changeListeners = new HashSet();

	/** The object that this environment centers on. */
	private Serializable theMainObject;

	/** The file owned by this serializable object. */
	private File file;

	/** The collection of file change listeners. */
	private Set fileListeners = new HashSet();

	/** The dirty bit. */
	private boolean dirty = false;
}
