import React from 'react';
import PropTypes from 'prop-types';
import { withStyles } from '@material-ui/core/styles';
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import Typography from '@material-ui/core/Typography';
import TextField from '@material-ui/core/TextField';
import List from '@material-ui/core/List';
import ListItem from '@material-ui/core/ListItem';
import { Button } from '@material-ui/core';

const styles = (theme) => ({
	root: {
		flexGrow: 1,
	},
	grow: {
		flexGrow: 1,
	},
	menuButton: {
		marginLeft: -12,
		marginRight: 20,
	},
	textField: {
    marginLeft: theme.spacing.unit,
    marginRight: theme.spacing.unit,
    width: 200,
  },
});

class App extends React.Component {
	constructor(props) {
		super(props);
		this.state = {
			items: ["", ""],
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
				<List>
				{
					this.state.items.map((item, index) => {
						return (
							<ListItem key={index}>
								<TextField
									label="item"

									className={classes.textField}
									value={item}
									onChange={this.handleChange(index)}
									margin="normal"
									/>
								<Button variant="contained" color="secondary" onClick={this.removeInput(index)}>Remove</Button>
							</ListItem>
						);
					})
				}
				</List>
				<Button variant="contained" onClick={this.addInput}>
					Add
				</Button>
				<Button variant="contained" color="primary" onClick={this.getOutput}>
					Plot
				</Button>
				<div>
					<img src={this.state.output} alt="output" />
				</div>
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
	addInput = () => {
		const items = this.state.items;
		items.push("");
		this.setState({items});
	}
	getOutput = () => {
		this.setState({ output: "https://chartio.com/images/tutorials/scatter-plot/Scatter-Plot-Weight-and-Height-Scatter-Plot-Trendline.png" })
	}
}

App.propTypes = {
	classes: PropTypes.object.isRequired,
};

export default withStyles(styles)(App);
