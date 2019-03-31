import React from 'react';
import PropTypes from 'prop-types';
import { withStyles } from '@material-ui/core/styles';
import { 
	AppBar, 
	Toolbar, 
	Typography, 
	TextField, 
	Table, TableBody, TableCell, TableRow, 
	IconButton, Button,
	Dialog, DialogActions, DialogContent, DialogContentText, DialogTitle,
} from '@material-ui/core';
import DeleteIcon from '@material-ui/icons/Delete';
import AddIcon from '@material-ui/icons/Add';

const styles = (theme) => ({
	root: {
		flexGrow: 1,
	},
	grow: {
		flexGrow: 1,
	},
	body: {
		padding: 20,
		maxWidth: 700,
		margin: "0 auto",
		right: 0, left: 0,
	},
	table: {
		maxWidth: 700,
	},
	removeButton: {
		float: "right",
	},
	textField: {
		marginLeft: theme.spacing.unit,
		marginRight: theme.spacing.unit,
		width: "100%",
	},
	addButton: {
		// float: "right",
	},
	plotButton: {
		margin: 5,
	},
});

class App extends React.Component {
	constructor(props) {
		super(props);
		this.state = {
			dialogTitle: "",
			dialogText: "",
			dialogOpened: false,
			teamSize: 2,
			items: [{name: "", idea: ""}, {name: "", idea: ""}],
			output: "",
		};
	}
	render () {
		const { classes } = this.props;
		return (
			<div className={classes.root}>
				<AppBar position="static">
					<Toolbar>
						<Typography variant="h6" color="inherit" className={classes.grow}>
							Scholar Match
						</Typography>
					</Toolbar>
				</AppBar>
				<div className={classes.body}>
					<TextField
						label="Team Size"
						defaultValue={this.state.teamSize}
						className={classes.teamSizeInput}
						onChange={this.handleSizeChange}
						margin="normal"
						/>
					<Table className={classes.table}>
						<TableBody>
							{this.state.items.map((item, index) => {
								return (
									<TableRow key={index}>
										<TableCell>
											<TextField
												label="Name"
												className={classes.textField}
												onChange={this.handleChange(index)}
												margin="normal"
												/>
										</TableCell>
										<TableCell>
											<TextField
												label="Idea"
												className={classes.textField}
												onChange={this.handleChange(index)}
												margin="normal"
												/>
										</TableCell>
										<TableCell>
											<IconButton className={classes.removeButton} variant="outlined" onClick={this.removeInput(index)}>
												<DeleteIcon />
											</IconButton>
										</TableCell>
									</TableRow>
								);
							})}
						</TableBody>
					</Table>
					<Button className={classes.addButton} onClick={this.addInput}> <AddIcon /> Add Person</Button>
					<br />
					<br />
					<Button className={classes.plotButton} variant="contained" color="primary" onClick={this.getOutput}>Plot</Button>
				<div>
					<img src={this.state.output} alt="output" />
				</div>
				</div>
				<Dialog
					open={this.state.dialogOpened}
					onClose={this.closeDialog}
					aria-labelledby="alert-dialog-title"
					aria-describedby="alert-dialog-description" >
				{this.state.dialogTitle.length > 0 &&
					<DialogTitle id="alert-dialog-title">{this.state.dialogTitle}</DialogTitle>}
				<DialogContent>
					<DialogContentText id="alert-dialog-description">
						{this.state.dialogText}
					</DialogContentText>
				</DialogContent>
				<DialogActions>
					<Button varient="contained" onClick={this.closeDialog} autoFocus>
					Close
					</Button>
				</DialogActions>
				</Dialog>
			</div>
		);
	}
	removeInput = index => () => {
		let items = this.state.items;
		items.splice(index, 1);
		this.setState({items});
	}
	handleChange = index => event => {
		const items = this.state.items;
		items[index] = event.target.value;
		this.setState({items});
	}
	handleSizeChange = event => {
		const stringValue = event.target.value;
		const value = parseInt(stringValue);
		this.setState({teamSize: isNaN(value) ? undefined : value });
	}
	addInput = () => {
		const items = this.state.items;
		items.push({name: "", idea: ""});
		this.setState({items});
	}
	getOutput = () => {
		if (typeof this.state.teamSize !== "number") {
			this.openDialog("Team size not valid.");
			return;
		}
		if (typeof this.state.teamSize < 2) {
			this.openDialog("Team size must be 2 or more!");
			return;
		}
		if (this.state.items.length % this.state.teamSize !== 0) {
			this.openDialog("You must have enough people to divide into even teams!");
			return;
		}
		this.setState({ output: "https://chartio.com/images/tutorials/scatter-plot/Scatter-Plot-Weight-and-Height-Scatter-Plot-Trendline.png" })
	}
	openDialog = (text, title="") => {
		this.setState({ dialogOpened: true, dialogText: text, dialogTitle: title });
	}
	closeDialog = () => {
		this.setState({ dialogOpened: false });
	}
}

App.propTypes = {
	classes: PropTypes.object.isRequired,
};

export default withStyles(styles)(App);
