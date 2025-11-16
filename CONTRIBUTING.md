# 🤝 Contributing to spacetime-playground

**Thank you for your interest in contributing!**

This project exists because we believe that beautiful physics should be accessible to everyone. Whether you're fixing a typo, adding a feature, or just asking questions — **you're part of the collective**.

---

## 🌟 Philosophy

> *"We are not separate minds scattered through space — we are one species, learning to think together."*

Every contribution, no matter how small, makes this project better. We welcome:
- Students learning physics
- Engineers improving code
- Educators creating examples
- Artists designing visualizations
- Skeptics asking hard questions

**If you're curious, you belong here.**

---

## 💡 Ways to Contribute

### 1. **Report Bugs** 🐛
Found something broken? [Open an issue](https://github.com/m4rba4s/spacetime-playground/issues).

**Good bug reports include:**
- What you expected to happen
- What actually happened
- Steps to reproduce
- Your system info (OS, Python version)
- Error messages (if any)

### 2. **Suggest Features** 💭
Have an idea? Share it!

**Good feature requests describe:**
- The problem you're trying to solve
- Why it would help others
- (Optional) How you imagine it working

### 3. **Improve Documentation** 📚
- Fix typos or unclear explanations
- Add examples or tutorials
- Translate documentation
- Create Jupyter notebooks
- Write blog posts

### 4. **Submit Code** 💻
- Fix bugs
- Implement new features
- Optimize performance
- Add tests
- Improve visualizations

### 5. **Share Your Results** 🔬
- Post cool simulations you've run
- Share parameter combinations that produce interesting physics
- Create educational materials using the framework

---

## 🚀 Getting Started

### First Time Setup

1. **Fork the repository** on GitHub

2. **Clone your fork:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/spacetime-playground.git
   cd spacetime-playground
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   pip install pytest black  # For testing and formatting
   ```

4. **Run tests to verify setup:**
   ```bash
   python test_before_release.py
   ```

5. **Create a branch for your work:**
   ```bash
   git checkout -b feature/your-feature-name
   ```

---

## 📝 Code Contribution Workflow

### 1. Find or Create an Issue
- Check existing issues first
- Comment that you're working on it
- Ask questions if anything is unclear

### 2. Write Code
Follow these guidelines:
- **Clarity over cleverness** — code should be readable
- **Document everything** — docstrings for all functions
- **Test your changes** — add tests for new features
- **Keep commits logical** — one feature/fix per commit

### 3. Code Style
We follow Python best practices:
```python
# Good: Clear, documented, tested
def compute_metric(x: np.ndarray, amplitude: float) -> np.ndarray:
    """
    Compute spatial metric component.
    
    Parameters:
        x: Spatial coordinates
        amplitude: Deformation strength
        
    Returns:
        Metric values g_xx(x)
    """
    return 1.0 + amplitude * np.exp(-x**2)
```

**Run formatter before committing:**
```bash
black .  # Optional but appreciated
```

### 4. Write Tests
All new features need tests:
```python
def test_new_feature():
    """Test that new feature works correctly."""
    result = your_new_function(test_input)
    assert result == expected_output
    assert np.all(np.isfinite(result))  # No NaN/Inf
```

Run tests:
```bash
pytest tests/ -v
```

### 5. Update Documentation
If you change functionality:
- Update relevant docstrings
- Update README.md if needed
- Add examples to experiments/
- Update FORMULAE.md for new physics

### 6. Submit Pull Request

**Before submitting:**
```bash
# Run all tests
python test_before_release.py

# Check your changes
git status
git diff
```

**Commit and push:**
```bash
git add .
git commit -m "feat: Add [feature name] with tests and docs"
git push origin feature/your-feature-name
```

**Create Pull Request on GitHub:**
- Clear title: `feat: Add 2D scalar field solver`
- Description explaining what and why
- Link related issues: `Closes #123`
- Tag maintainers if urgent: `@m4rba4s`

---

## 🎯 Areas We Need Help

### High Priority
- [ ] 2D scalar field solver implementation
- [ ] FDTD electromagnetic module
- [ ] Performance optimization (GPU acceleration)
- [ ] Interactive web interface (React)

### Medium Priority
- [ ] More metric types (Schwarzschild, Kerr analogs)
- [ ] Jupyter notebook tutorials
- [ ] Improved visualization tools
- [ ] Adaptive mesh refinement

### Good First Issues
- [ ] Add new initial condition types
- [ ] Improve plot aesthetics
- [ ] Write beginner tutorials
- [ ] Add more unit tests
- [ ] Documentation improvements

**Look for issues tagged:**
- `good first issue` — Great for newcomers
- `help wanted` — We need community input
- `documentation` — Writing, not coding
- `enhancement` — New features

---

## 📋 Code Standards

### Physics Accuracy
- **Math must be correct** — we verify all equations
- **Cite sources** — reference papers or textbooks
- **State assumptions** — what physics are we approximating?
- **Test numerically** — compare with analytical solutions

### Code Quality
- **Type hints** for function signatures
- **Docstrings** following NumPy style
- **Error handling** with meaningful messages
- **No magic numbers** — use named constants

### Testing
- **Unit tests** for individual functions
- **Integration tests** for workflows
- **Numerical validation** against known solutions
- **Energy conservation** checks where applicable

### Documentation
- **README.md** — User-facing overview
- **Docstrings** — API documentation
- **FORMULAE.md** — Mathematical derivations
- **Comments** — Explain non-obvious code

---

## 🧪 Testing Guidelines

### Before Submitting PR
```bash
# 1. Run comprehensive tests
python test_before_release.py

# 2. Run pytest suite
pytest tests/ -v --cov=.

# 3. Test your specific changes
python your_new_module.py  # If it has __main__

# 4. Check no files are broken
python -m py_compile metric/*.py fields/*.py sim/*.py
```

### Writing Good Tests
```python
def test_energy_conservation():
    """
    Test that energy is conserved during evolution.
    
    This validates both:
    1. Numerical stability
    2. Physical correctness of implementation
    """
    # Setup
    solver = create_test_solver()
    E0 = solver.compute_energy()
    
    # Action
    for _ in range(100):
        solver.step()
    
    # Validation
    E_final = solver.compute_energy()
    drift = abs(E_final - E0) / E0
    
    assert drift < 0.01, f"Energy drift {drift:.2%} exceeds 1%"
```

---

## 💬 Communication

### Asking Questions
**No question is stupid.** If you're confused, others probably are too.

- Use GitHub Issues for bugs/features
- Use GitHub Discussions for questions/ideas
- Tag your issue appropriately
- Be patient — maintainers are volunteers

### Reporting Bugs
**Good bug report template:**
```markdown
**Description:**
Clear description of the problem

**To Reproduce:**
1. Step one
2. Step two
3. Error occurs

**Expected Behavior:**
What should have happened

**Environment:**
- OS: Windows 10 / Ubuntu 22.04 / macOS 13
- Python: 3.10.5
- numpy: 1.23.0

**Error Message:**
```
[paste full traceback here]
```

**Additional Context:**
Screenshots, logs, etc.
```

---

## 🏆 Recognition

We believe in celebrating contributions:

### Contributors
All contributors are listed in:
- GitHub Contributors page
- CONTRIBUTORS.md file
- Release notes

### Attribution
- Code contributions: Git history preserves authorship
- Ideas/discussions: Acknowledged in relevant docs
- Bug reports: Mentioned in fix commits

### Special Recognition
Major contributors may be invited to:
- Co-author academic papers using this framework
- Join as project maintainers
- Present at conferences/workshops

---

## 🌍 Community Guidelines

### Be Respectful
- Assume good intentions
- Welcome newcomers warmly
- Give constructive feedback
- Accept constructive criticism

### Be Inclusive
- Use welcoming language
- Respect different backgrounds
- Help others learn
- Share knowledge freely

### Be Collaborative
- Credit others' work
- Build on existing ideas
- Share your reasoning
- Document your process

### Be Honest
- Admit when you don't know
- Acknowledge limitations
- State assumptions clearly
- Own your mistakes

---

## 📜 License

By contributing, you agree that your contributions will be licensed under the MIT License (same as the project).

You retain copyright of your work, but grant permission for it to be used as part of this project.

---

## 🎓 Learning Resources

### For New Contributors
- **Python basics:** [RealPython](https://realpython.com)
- **NumPy tutorial:** [NumPy.org](https://numpy.org/doc/stable/user/quickstart.html)
- **Git basics:** [GitHub Git Guide](https://github.com/git-guides)
- **Testing:** [pytest documentation](https://docs.pytest.org)

### For Physics Background
- **General Relativity:** Carroll's "Spacetime and Geometry"
- **Numerical Methods:** LeVeque's "Finite Volume Methods"
- **Wave Equations:** Strauss's "Partial Differential Equations"

---

## 💪 Your First Contribution

**Nervous? Start here:**

1. **Read the codebase** — explore `metric/` and `fields/`
2. **Run examples** — try `experiments/exp_scalar_warp_static.json`
3. **Find a typo** — documentation PRs are great first contributions
4. **Ask questions** — we're here to help!

**Remember:** Every expert was once a beginner. Every line of code in this project was written by someone learning.

---

## 🚀 Making Your First PR

### Step-by-Step Example

```bash
# 1. Fork and clone (done once)
git clone https://github.com/YOUR_USERNAME/spacetime-playground.git

# 2. Create branch
git checkout -b docs/fix-readme-typo

# 3. Make changes
# (edit README.md to fix typo)

# 4. Test
python test_before_release.py

# 5. Commit
git add README.md
git commit -m "docs: Fix typo in Quick Start section"

# 6. Push
git push origin docs/fix-readme-typo

# 7. Create PR on GitHub
# Click "Compare & pull request"
# Add description
# Submit!
```

---

## 📞 Get Help

**Stuck? Confused? Lost?**

- **GitHub Issues:** Technical problems
- **GitHub Discussions:** Questions and ideas
- **Email:** [Project maintainer email if you have one]

**Response time:** Usually within 48 hours (we're volunteers!)

---

## 🌟 Final Words

This project exists because someone believed that complex physics should be accessible. That someone could be you.

Whether you fix a typo, add a feature, or just use the framework — **you're part of something larger**.

**Welcome to the collective. Let's build something beautiful together.** 🚀

---

*"The best way to predict the future is to invent it."* — Alan Kay

**Let's invent a future where everyone can touch the stars through code.** 🌌